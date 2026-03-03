import { FraudFactor, FraudResult } from "../types";

const API_BASE =
  (import.meta as any)?.env?.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

// ----------------------------
// Types
// ----------------------------

type ApiErrorPayload = {
  detail?: string;
  error?: string;
  message?: string;
};

export type NokiaFullScanResponse = {
  ok?: boolean;
  phoneNumber?: string;
  error?: string;
  scan?: {
    simSwap?: { swapped?: boolean };
    simSwapDate?: { latestSimChange?: string };

    deviceSwap?: { swapped?: boolean };
    deviceSwapDate?: { latestDeviceChange?: string };

    numberRecycling?: { phoneNumberRecycled?: boolean };

    location?: {
      lastLocationTime?: string;
      area?: {
        areaType?: string;
        radius?: number;
        center?: { latitude?: number; longitude?: number };
      };
    };

    // Future (agent-provided)
    score?: number;
    riskLevel?: "low" | "medium" | "high" | "critical";
    factors?: FraudFactor[];
    details?: string;
    carrier?: string;
    locationName?: string;

    // Optional future flags
    isVoip?: boolean;
    locationAnomaly?: boolean;
    kycMatch?: boolean;

    // Optional ids/timestamps if backend adds them
    id?: string;
    timestamp?: number;
  };
};

// ----------------------------
// Helpers
// ----------------------------

async function parseError(res: Response): Promise<string> {
  try {
    const j = (await res.json()) as ApiErrorPayload;
    return j.detail ?? j.error ?? j.message ?? `Request failed (${res.status})`;
  } catch {
    try {
      const t = await res.text();
      return t || `Request failed (${res.status})`;
    } catch {
      return `Request failed (${res.status})`;
    }
  }
}

function deriveRiskLevel(score: number): FraudResult["riskLevel"] {
  if (score < 30) return "low";
  if (score < 60) return "medium";
  if (score < 85) return "high";
  return "critical";
}

const clamp = (n: number, min = 0, max = 100) => Math.max(min, Math.min(max, n));

function statusFromValue(v: number): FraudFactor["status"] {
  if (v >= 80) return "danger";
  if (v >= 55) return "warning";
  return "safe";
}

function randomBetween(min: number, max: number): number {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function build3Factors(flags: {
  simSwap: boolean;
  deviceSwap: boolean;
  numberRecycling: boolean;
}): FraudFactor[] {

  // Si flag = true → alt risc random
  // Si flag = false → baix risc random

  const simSwap = flags.simSwap
    ? randomBetween(80, 95)
    : randomBetween(5, 20);

  const deviceSwap = flags.deviceSwap
    ? randomBetween(70, 90)
    : randomBetween(5, 20);

  const recycling = flags.numberRecycling
    ? randomBetween(60, 85)
    : randomBetween(5, 20);

  return [
    { label: "SIM Swap Risk", value: simSwap, status: statusFromValue(simSwap) },
    { label: "Device Swap Risk", value: deviceSwap, status: statusFromValue(deviceSwap) },
    { label: "Number Recycling Risk", value: recycling, status: statusFromValue(recycling) },
  ];
}

function scoreFrom3Factors(factors: FraudFactor[]): number {
  const weights: Record<string, number> = {
    "SIM Swap Risk": 0.45,
    "Device Swap Risk": 0.30,
    "Number Recycling Risk": 0.25,
  };

  const total = factors.reduce((acc, f) => acc + (weights[f.label] ?? 0), 0) || 1;

  const weighted = factors.reduce((acc, f) => {
    const w = weights[f.label] ?? 0;
    return acc + f.value * w;
  }, 0);

  return clamp(Math.round(weighted / total));
}

function formatLocation(scan: NokiaFullScanResponse["scan"]): string {
  if (typeof scan?.locationName === "string" && scan.locationName.trim()) {
    return scan.locationName;
  }

  const lat = scan?.location?.area?.center?.latitude;
  const lng = scan?.location?.area?.center?.longitude;

  if (typeof lat === "number" && typeof lng === "number") {
    return `${lat.toFixed(4)}, ${lng.toFixed(4)}`;
  }

  return "Unknown";
}

/**
 * Convert Nokia "full-scan" response into a UI-friendly FraudResult.
 * Defensive mapping: always returns safe fields so UI never crashes.
 * NOTE: score/riskLevel are mocked until agent scoring is enabled.
 */
export function mapNokiaScanToFraudResult(
  phoneNumber: string,
  res: NokiaFullScanResponse
): FraudResult {
  const scan = res.scan ?? {};

  const simSwapHistory = !!scan.simSwap?.swapped;
  const deviceSwap = !!scan.deviceSwap?.swapped;
  const numberRecycling = !!scan.numberRecycling?.phoneNumberRecycled;

  const isVoip = !!scan.isVoip;
  const locationAnomaly = !!scan.locationAnomaly;

  
  const kycMatch = typeof scan.kycMatch === "boolean" ? scan.kycMatch : true;

  // 1) Factors: backend factors respected; else generate 3-factor model
  const factors: FraudFactor[] = Array.isArray(scan.factors)
    ? scan.factors
    : build3Factors({
        simSwap: simSwapHistory,
        deviceSwap,
        numberRecycling,
      });


  // 2) Score rules:
  // - If KYC is explicitly false => force score to 10 (as requested)
  // - Else if backend provides score => use it
  // - Else derive score from the 3 factors
  const score =
    kycMatch === false
      ? 10
      : typeof scan.score === "number"
      ? scan.score
      : scoreFrom3Factors(factors);

  // 3) Risk level from score (or backend riskLevel if provided)
  const riskLevel = scan.riskLevel ?? deriveRiskLevel(score);

  return {
    id: scan.id ?? crypto.randomUUID(),
    phoneNumber: res.phoneNumber ?? phoneNumber,
    score,
    timestamp: scan.timestamp ?? Date.now(),

    riskLevel,
    factors,

    details:
      scan.details ??
      "Signals collected from Nokia Network-as-Code. Agent scoring not enabled yet.",

    carrier: scan.carrier ?? "Unknown",
    location: formatLocation(scan),

    isVoip: !!scan.isVoip,
    simSwapHistory,
    deviceSwap,
    locationAnomaly: !!scan.locationAnomaly,
    numberRecycling,
    kycMatch: typeof scan.kycMatch === "boolean" ? scan.kycMatch : true,

    scanRaw: scan,
    locationRaw: scan.location,
    simSwapRaw: scan.simSwap,
    deviceSwapRaw: scan.deviceSwap,
    numberRecyclingRaw: scan.numberRecycling,
  } as FraudResult;
}

// ----------------------------
// API
// ----------------------------

/**
 * 1) Call backend to retrieve Nokia signals (full-scan).
 * 2) Map to FraudResult with safe fallbacks.
 * 3) (Later) send result.scanRaw to your agent backend.
 */
export async function scanFraudByPhone(phoneNumber: string): Promise<FraudResult> {
  const res = await fetch(`${API_BASE}/api/nokia/full-scan/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ phoneNumber }),
  });

  if (!res.ok) throw new Error(await parseError(res));

  const data = (await res.json()) as NokiaFullScanResponse;

  if (data.ok === false) {
    throw new Error(data.error ?? "Scan failed");
  }

  return mapNokiaScanToFraudResult(phoneNumber, data);
}

/**
 * Agent backend (stub for now).
 * Later: POST /api/agent/score/ with { phoneNumber, scan: <raw_nokia_scan> }.
 */
export async function scoreWithAgent(_: {
  phoneNumber: string;
  scan: unknown;
}): Promise<Partial<FraudResult>> {
  return { details: "Agent scoring not enabled yet (stub)." };
}