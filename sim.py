import http.client
import json
from supabase import create_client, Client

# -------- CONFIG --------

RAPIDAPI_KEY = "6b5cf197c0mshe27c521aaca32e8p1ac9aejsndc736cfb17f7"
HOST = "network-as-code.p-eu.rapidapi.com"

SUPABASE_URL = "https://cyvyilelgipfcrwzssmv.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN5dnlpbGVsZ2lwZmNyd3pzc212Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MjQ1MDA1NSwiZXhwIjoyMDg4MDI2MDU1fQ.u4vj6cDwyTHTTEAjUNDUcymCx0LK4VQ6n8zrvouNZFQ"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

headers = {
    'x-rapidapi-key': RAPIDAPI_KEY,
    'x-rapidapi-host': "network-as-code.nokia.rapidapi.com",
    'Content-Type': "application/json"
}

phone_number = "+99999991000"

# ---------- SIM SWAP CHECK ----------

conn_sim = http.client.HTTPSConnection(HOST)

payload_sim_check = json.dumps({
    "phoneNumber": phone_number,
    "maxAge": 10080
})

conn_sim.request(
    "POST",
    "/passthrough/camara/v1/sim-swap/sim-swap/v0/check",
    payload_sim_check,
    headers
)

res_sim = conn_sim.getresponse()
raw_sim_response = res_sim.read().decode("utf-8")
data_sim = json.loads(raw_sim_response)

print("SIM SWAP CHECK:")
print(data_sim)

last_sim_swap_date = None

# Si swapped es true → recuperar fecha
if data_sim.get("swapped"):

    conn_sim_retrieve = http.client.HTTPSConnection(HOST)

    payload_sim_retrieve = json.dumps({
        "phoneNumber": phone_number
    })

    conn_sim_retrieve.request(
        "POST",
        "/passthrough/camara/v1/sim-swap/sim-swap/v0/retrieve-date",
        payload_sim_retrieve,
        headers
    )

    res_sim_date = conn_sim_retrieve.getresponse()
    raw_sim_date_response = res_sim_date.read().decode("utf-8")
    data_sim_date = json.loads(raw_sim_date_response)

    print("SIM SWAP LAST DATE:")
    print(data_sim_date)

    last_sim_swap_date = data_sim_date.get("lastSimSwapDate")


# -------- INSERTAR EN SUPABASE --------

insert_data = {
    "phone_number": phone_number,
    "swapped": data_sim.get("swapped", False),
    "last_sim_swap_date": last_sim_swap_date,
    "max_age_minutes": 10080,
    "raw_response": data_sim
}

response = supabase.table("sim_swap_history").insert(insert_data).execute()

print("\nGUARDADO EN SUPABASE:")
print(response)