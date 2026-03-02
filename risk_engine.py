import os
import json
import math
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional, Tuple

from supabase import create_client, Client

# Wrappers que ya tenéis
from numrecapi import check_number_recycling
from kyc_match import kyc_match

# OpenAI
from openai import OpenAI




if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Faltan SUPABASE_URL / SUPABASE_KEY en variables de entorno.")
if not OPENAI_API_KEY:
    raise RuntimeError("Falta OPENAI_API_KEY en variables de entorno.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
openai_client = OpenAI(api_key=OPENAI_API_KEY)


# -----------------------
# BD Helpers
# -----------------------
def get_last_n(table: str, select_fields: str, n: int = 20) -> List[Dict[str, Any]]:
    resp = (
        supabase.table(table)
        .select(select_fields)
        .order("created_at", desc=True)
        .limit(n)
        .execute()
    )
    return resp.data or []


# -----------------------
# Time helpers
# -----------------------
def parse_iso(dt_str: str) -> datetime:
    # soporta "+00:00" o "Z"
    return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))


def minutes_since(iso_dt: Optional[str]) -> Optional[int]:
    if not iso_dt:
        return None
    try:
        dt = parse_iso(iso_dt)
        now = datetime.now(timezone.utc)
        return int((now - dt).total_seconds() // 60)
    except Exception:
        return None


def count_within_days(iso_dates: List[str], days: int) -> int:
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=days)
    c = 0
    for s in iso_dates:
        try:
            if parse_iso(s) >= cutoff:
                c += 1
        except Exception:
            pass
    return c


# -----------------------
# Geo helpers (Haversine)
# -----------------------
def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = (math.sin(dphi / 2) ** 2) + math.cos(phi1) * math.cos(phi2) * (math.sin(dlambda / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def max_geo_jump_km(locations: List[Dict[str, float]], max_points: int = 6) -> float:
    """
    Calcula el salto máximo entre puntos consecutivos en las últimas N ubicaciones.
    locations: [{"lat": .., "lon": ..}, ...] en orden "más reciente primero".
    """
    locs = locations[:max_points]
    if len(locs) < 2:
        return 0.0

    max_jump = 0.0
    for i in range(len(locs) - 1):
        a = locs[i]
        b = locs[i + 1]
        try:
            jump = haversine_km(float(a["lat"]), float(a["lon"]), float(b["lat"]), float(b["lon"]))
            if jump > max_jump:
                max_jump = jump
        except Exception:
            pass
    return float(round(max_jump, 2))


# -----------------------
# KYC helpers
# -----------------------
def normalize_bool_str(v: Any) -> Optional[bool]:
    if isinstance(v, bool):
        return v
    if isinstance(v, str):
        lv = v.lower().strip()
        if lv == "true":
            return True
        if lv == "false":
            return False
    return None


def kyc_match_ratio_and_failed_fields(kyc: Dict[str, Any]) -> Tuple[float, List[str]]:
    vals: List[bool] = []
    failed: List[str] = []

    for k, v in kyc.items():
        b = normalize_bool_str(v)
        if b is None:
            continue
        vals.append(b)
        if b is False:
            failed.append(k)

    if not vals:
        return 0.0, []
    ratio = sum(1 for x in vals if x) / len(vals)
    return float(round(ratio, 3)), failed[:15]


# -----------------------
# Prompt schema (output fijo) + timestamps obligatorios
# -----------------------
RISK_SCHEMA = {
    "name": "transaction_risk_decision",
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "allow_transaction": {"type": "boolean"},
            "decision": {"type": "string", "enum": ["ALLOW", "STEP_UP", "BLOCK"]},
            "risk_score": {"type": "integer", "minimum": 0, "maximum": 100},
            "reasons": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 1,
                "maxItems": 10
            },
            # ✅ NUEVOS CAMPOS (obligatorios; ISO 8601 o null)
            "last_sim_swap_timestamp": {"type": ["string", "null"]},
            "last_device_swap_timestamp": {"type": ["string", "null"]}
        },
        "required": [
            "allow_transaction",
            "decision",
            "risk_score",
            "reasons",
            "last_sim_swap_timestamp",
            "last_device_swap_timestamp"
        ]
    }
}


def build_risk_payload(phone: str, transaction: Dict[str, Any]) -> Dict[str, Any]:
    # Históricos desde BD
    device_rows = get_last_n("device_swap_history", "last_device_swap_date", 20)
    sim_rows = get_last_n("sim_swap_history", "last_sim_swap_date", 20)
    loc_rows = get_last_n("location_history", "latitude, longitude, created_at", 20)

    device_dates = [r.get("last_device_swap_date") for r in device_rows if r.get("last_device_swap_date")]
    sim_dates = [r.get("last_sim_swap_date") for r in sim_rows if r.get("last_sim_swap_date")]

    # ✅ Ordenar fechas para que el "último" sea el más reciente
    device_dates_sorted = sorted(device_dates, key=parse_iso, reverse=True)
    sim_dates_sorted = sorted(sim_dates, key=parse_iso, reverse=True)

    last_sim_swap_ts = sim_dates_sorted[0] if sim_dates_sorted else None
    last_device_swap_ts = device_dates_sorted[0] if device_dates_sorted else None

    locations = [
        {"lat": r.get("latitude"), "lon": r.get("longitude")}
        for r in loc_rows
        if r.get("latitude") is not None and r.get("longitude") is not None
    ]

    # Señales directas (tiempo real)
    specified_date = transaction.get("number_recycling_specified_date", "2024-10-31")
    number_recycling = check_number_recycling(phone, specified_date)

    # KYC
    kyc_payload = {
        "phoneNumber": phone,
        "idDocument": transaction.get("idDocument", "UNKNOWN"),
        "name": transaction.get("name", "UNKNOWN"),
        "givenName": transaction.get("givenName", "UNKNOWN"),
        "familyName": transaction.get("familyName", "UNKNOWN"),
        "address": transaction.get("address", "UNKNOWN"),
        "birthdate": transaction.get("birthdate", "UNKNOWN"),
        "email": transaction.get("email", "UNKNOWN"),
        "country": transaction.get("country", "UNKNOWN"),
    }
    kyc = kyc_match(kyc_payload)

    kyc_ratio, kyc_failed = kyc_match_ratio_and_failed_fields(kyc)

    features = {
        "sim_swap_minutes_since_last": minutes_since(last_sim_swap_ts),
        "device_swap_minutes_since_last": minutes_since(last_device_swap_ts),
        "sim_swaps_last_7d": count_within_days(sim_dates_sorted, 7),
        "sim_swaps_last_30d": count_within_days(sim_dates_sorted, 30),
        "device_swaps_last_30d": count_within_days(device_dates_sorted, 30),
        "phoneNumberRecycled": bool(number_recycling.get("phoneNumberRecycled", False)),
        "kyc_match_ratio": kyc_ratio,
        "kyc_failed_fields": kyc_failed,
        "geo_jump_km_last_points": max_geo_jump_km(locations),
        # ✅ NUEVOS: timestamps ISO 8601
        "last_sim_swap_timestamp": last_sim_swap_ts,
        "last_device_swap_timestamp": last_device_swap_ts,
    }

    payload = {
        "transaction": transaction,
        "signals_raw": {
            # ✅ también dejamos ordenado para coherencia
            "sim_swap_dates_last_20": sim_dates_sorted[:20],
            "device_swap_dates_last_20": device_dates_sorted[:20],
            "locations_last_20": locations[:20],
            "number_recycling": number_recycling,
            "kyc_match": kyc
        },
        "features": features
    }
    return payload


def call_risk_llm(payload: Dict[str, Any]) -> Dict[str, Any]:
    system = (
        "Eres un motor de riesgo antifraude para transacciones bancarias. "
        "Devuelve SOLO JSON válido según el esquema. "
        "Decide ALLOW, STEP_UP o BLOCK. "
        "Considera especialmente: SIM swap reciente, device swap reciente, number recycled, mismatches de KYC, saltos geográficos. "
        "IMPORTANTE: Rellena siempre last_sim_swap_timestamp y last_device_swap_timestamp usando los valores del payload (features). "
        "Las razones deben ser concretas, cortas y accionables."
    )

    user = {
        "task": "Evalúa el riesgo y toma una decisión final para permitir o no la transacción.",
        "payload": payload
    }

    resp = openai_client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": json.dumps(user, ensure_ascii=False)}
        ],
        response_format={"type": "json_schema", "json_schema": RISK_SCHEMA},
        temperature=0.2
    )

    content = resp.choices[0].message.content
    return json.loads(content)


def fallback_rules(features: Dict[str, Any]) -> Dict[str, Any]:
    sim_m = features.get("sim_swap_minutes_since_last")
    dev_m = features.get("device_swap_minutes_since_last")
    recycled = features.get("phoneNumberRecycled", False)
    kyc_r = features.get("kyc_match_ratio", 0.0)
    geo_jump = features.get("geo_jump_km_last_points", 0.0)

    takeover_like = (
        recycled is True or
        (sim_m is not None and sim_m < 120) or
        (kyc_r is not None and kyc_r < 0.3) or
        (geo_jump is not None and geo_jump > 500)
    )

    if takeover_like:
        return {
            "allow_transaction": False,
            "decision": "BLOCK",
            "risk_score": 90,
            "reasons": [
                "Fallback: señales fuertes de takeover",
                f"recycled={recycled}, sim_minutes={sim_m}, kyc_ratio={kyc_r}, geo_jump_km={geo_jump}"
            ],
            # ✅ obligatorios en schema
            "last_sim_swap_timestamp": features.get("last_sim_swap_timestamp"),
            "last_device_swap_timestamp": features.get("last_device_swap_timestamp"),
        }

    medium = (
        (dev_m is not None and dev_m < 1440) or
        (features.get("sim_swaps_last_7d", 0) >= 2) or
        (features.get("device_swaps_last_30d", 0) >= 2)
    )

    if medium:
        return {
            "allow_transaction": False,
            "decision": "STEP_UP",
            "risk_score": 55,
            "reasons": [
                "Fallback: riesgo moderado, requiere verificación adicional"
            ],
            "last_sim_swap_timestamp": features.get("last_sim_swap_timestamp"),
            "last_device_swap_timestamp": features.get("last_device_swap_timestamp"),
        }

    return {
        "allow_transaction": True,
        "decision": "ALLOW",
        "risk_score": 15,
        "reasons": [
            "Fallback: no se detectan señales relevantes de riesgo"
        ],
        "last_sim_swap_timestamp": features.get("last_sim_swap_timestamp"),
        "last_device_swap_timestamp": features.get("last_device_swap_timestamp"),
    }


def evaluate_transaction(phone: str, transaction: Dict[str, Any]) -> Dict[str, Any]:
    payload = build_risk_payload(phone, transaction)

    try:
        decision = call_risk_llm(payload)
    except Exception as e:
        decision = fallback_rules(payload["features"])
        decision["reasons"].append(f"OpenAI error: {type(e).__name__}")

    # Guard-rails: coherencia allow_transaction vs decision
    decision["allow_transaction"] = (decision["decision"] == "ALLOW")

    # ✅ Forzar consistencia: estos timestamps salen SIEMPRE desde backend (no inventados)
    decision["last_sim_swap_timestamp"] = payload["features"].get("last_sim_swap_timestamp")
    decision["last_device_swap_timestamp"] = payload["features"].get("last_device_swap_timestamp")

    # Para frontend: señales reales
    decision["signals_used"] = payload["features"]
    decision["transaction_id"] = transaction.get("transaction_id")
    decision["timestamp"] = datetime.now().astimezone().isoformat()

    return decision