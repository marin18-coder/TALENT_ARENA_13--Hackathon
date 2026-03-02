from supabase import create_client, Client
from number_recycling import check_number_recycling
from kyc_match import kyc_match
import json

# -------- CONFIG --------

SUPABASE_URL = "https://cyvyilelgipfcrwzssmv.supabase.co"
SUPABASE_KEY = "TU_SERVICE_ROLE_KEY_AQUI"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------- DEVICE SWAP HISTORY ----------

device_swap_response = (
    supabase
    .table("device_swap_history")
    .select("last_device_swap_date")
    .order("created_at", desc=True)
    .limit(20)
    .execute()
)

device_swap_data = device_swap_response.data or []

# ---------- LOCATION HISTORY ----------

location_response = (
    supabase
    .table("location_history")
    .select("latitude, longitude")
    .order("created_at", desc=True)
    .limit(20)
    .execute()
)

location_data = location_response.data or []

# ---------- SIM SWAP HISTORY ----------

sim_swap_response = (
    supabase
    .table("sim_swap_history")
    .select("last_sim_swap_date")
    .order("created_at", desc=True)
    .limit(20)
    .execute()
)

sim_swap_data = sim_swap_response.data or []

# ---------- NUMBER RECYCLED ----------

phone = "+99999991000"
date = "2024-10-31"

number_recycled_result = check_number_recycling(phone, date)

# Aseguramos que sea 0 o 1
number_recycled_flag = 1 if number_recycled_result else 0


# ---------- KYC MATCH ----------

user_data = {
    "phoneNumber": "+99999991000",
    "idDocument": "66666666q",
    "name": "Federica Sanchez Arjona",
    "givenName": "Federica",
    "familyName": "Sanchez Arjona",
    "nameKanaHankaku": "federica",
    "nameKanaZenkaku": "Ｆｅｄｅｒｉｃａ",
    "middleNames": "Sanchez",
    "familyNameAtBirth": "YYYY",
    "address": "Tokyo-to Chiyoda-ku Iidabashi 3-10-10",
    "streetName": "Nicolas Salmeron",
    "streetNumber": "4",
    "postalCode": "1028460",
    "region": "Tokyo",
    "locality": "ZZZZ",
    "country": "JP",
    "houseNumberExtension": "VVVV",
    "birthdate": "1978-08-22",
    "email": "abc@example.com",
    "gender": "OTHER"
}

kyc_result = kyc_match(user_data)

# Aseguramos 0 o 1
kyc_match_flag = 1 if kyc_result else 0


# ---------- CONSTRUIR JSON FINAL ----------

fraud_payload = {
    "table_a_last20": device_swap_data,
    "table_b_last20": location_data,
    "table_c_last20": sim_swap_data,
    "number_recycled": number_recycled_flag,
    "kyc_match": kyc_match_flag
}

# Devuelve JSON listo para enviar a la IA
print(json.dumps(fraud_payload, indent=2))