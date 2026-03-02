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

# ---------- DEVICE SWAP CHECK ----------

conn_device = http.client.HTTPSConnection(HOST)

payload_device_check = json.dumps({
    "phoneNumber": phone_number,
    "maxAge": 10080 
})

conn_device.request(
    "POST",
    "/passthrough/camara/v1/device-swap/device-swap/v1/check",
    payload_device_check,
    headers
)

res_device = conn_device.getresponse()
raw_device_response = res_device.read().decode("utf-8")
data_device = json.loads(raw_device_response)

print("DEVICE SWAP CHECK:")
print(data_device)

last_device_swap_date = None

# Si swapped es true → recuperar fecha
if data_device.get("swapped"):

    conn_device_retrieve = http.client.HTTPSConnection(HOST)

    payload_device_retrieve = json.dumps({
        "phoneNumber": phone_number
    })

    conn_device_retrieve.request(
        "POST",
        "/passthrough/camara/v1/device-swap/device-swap/v1/retrieve-date",
        payload_device_retrieve,
        headers
    )

    res_device_date = conn_device_retrieve.getresponse()
    raw_device_date_response = res_device_date.read().decode("utf-8")
    data_device_date = json.loads(raw_device_date_response)

    print("DEVICE SWAP LAST DATE:")
    print(data_device_date)

    last_device_swap_date = data_device_date.get("lastDeviceSwapDate")


# -------- INSERTAR EN SUPABASE --------

insert_data = {
    "phone_number": phone_number,
    "swapped": data_device.get("swapped", False),
    "last_device_swap_date": last_device_swap_date,
    "max_age_minutes": 10080,
    "raw_response": data_device
}

response = supabase.table("device_swap_history").insert(insert_data).execute()

print("\nGUARDADO EN SUPABASE:")
print(response)