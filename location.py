import http.client
import json
from supabase import create_client, Client

# -------- CONFIG --------

RAPIDAPI_KEY = "6b5cf197c0mshe27c521aaca32e8p1ac9aejsndc736cfb17f7"
HOST = "network-as-code.p-eu.rapidapi.com"

SUPABASE_URL = "https://cyvyilelgipfcrwzssmv.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN5dnlpbGVsZ2lwZmNyd3pzc212Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MjQ1MDA1NSwiZXhwIjoyMDg4MDI2MDU1fQ.u4vj6cDwyTHTTEAjUNDUcymCx0LK4VQ6n8zrvouNZFQ"

phone_number = "+99999991000"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

headers = {
    'x-rapidapi-key': RAPIDAPI_KEY,
    'x-rapidapi-host': "network-as-code.nokia.rapidapi.com",
    'Content-Type': "application/json"
}

# ---------- LLAMADA A LA API ----------

conn = http.client.HTTPSConnection(HOST)

payload = json.dumps({
    "device": {
        "phoneNumber": phone_number
    },
    "maxAge": 60
})

conn.request(
    "POST",
    "/location-retrieval/v0/retrieve",
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

latitude = data.get("latitude")
longitude = data.get("longitude")
accuracy = data.get("accuracy")
location_timestamp = data.get("timestamp")

if not latitude or not longitude:
    print("No hay ubicación disponible.")
    exit()

# ---------- INSERTAR SIEMPRE ----------

insert_data = {
    "phone_number": phone_number,
    "latitude": latitude,
    "longitude": longitude,
    "accuracy": accuracy,
    "location_timestamp": location_timestamp,
    "raw_response": data
}

response = supabase.table("location_history").insert(insert_data).execute()

print("Ubicación guardada correctamente.")
print(response)