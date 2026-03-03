import http.client
import json
from supabase import create_client, Client
import settings as s
# -------- CONFIG --------

RAPIDAPI_KEY = s.x_rapid_key
HOST = "network-as-code.p-eu.rapidapi.com"

SUPABASE_URL = "https://cyvyilelgipfcrwzssmv.supabase.co"
SUPABASE_KEY = s.SUPABASE_KEY
phone_number = "+99999991000"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

headers = {
    'x-rapidapi-key': RAPIDAPI_KEY,
    'x-rapidapi-host': "network-as-code.nokia.rapidapi.com",
    'Content-Type': "application/json"
}

# ---------- 1️⃣ LLAMAR A LA API ----------

conn = http.client.HTTPSConnection(HOST)

payload = json.dumps({
    "phoneNumber": phone_number
})

conn.request(
    "POST",
    "/passthrough/camara/v1/sim-swap/sim-swap/v0/retrieve-date",
    payload,
    headers
)

res = conn.getresponse()
raw_response = res.read().decode("utf-8")

if res.status != 200:
    print("Error API:", raw_response)
    exit()

print("RAW RESPONSE:", raw_response)

data = json.loads(raw_response)
api_date = data.get("lastSimSwapDate")

print("Fecha API:", api_date)

if not api_date:
    print("No hay fecha de SIM swap.")
    exit()

# ---------- 2️⃣ OBTENER ÚLTIMA FECHA EN BD ----------

response = (
    supabase
    .table("sim_swap_history")
    .select("last_sim_swap_date")
    .eq("phone_number", phone_number)
    .order("created_at", desc=True)
    .limit(1)
    .execute()
)

db_date = None
if response.data and len(response.data) > 0:
    db_date = response.data[0]["last_sim_swap_date"]

print("Fecha BD:", db_date)

# ---------- 3️⃣ COMPARAR E INSERTAR ----------

if db_date != api_date:
    print("Nueva fecha detectada. Insertando en BD...")

    insert_data = {
        "phone_number": phone_number,
        "swapped": True,
        "last_sim_swap_date": api_date,
        "max_age_minutes": None,
        "raw_response": data
    }

    supabase.table("sim_swap_history").insert(insert_data).execute()
    print("Insertado correctamente.")
else:
    print("No hay cambios. No se inserta nada.")