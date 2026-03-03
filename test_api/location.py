import http.client
import json
from supabase import create_client, Client
import settings as s
# -------- CONFIG --------

HOST = "network-as-code.p-eu.rapidapi.com"
SUPABASE_URL = "https://cyvyilelgipfcrwzssmv.supabase.co"
phone_number = "+99999991000"

supabase: Client = create_client(SUPABASE_URL, s.SUPABASE_KEY)

headers = {
    'x-rapidapi-key': s.x_rapid_key,
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

last_location_time = data.get("lastLocationTime")

area = data.get("area", {})
center = area.get("center", {})

latitude = center.get("latitude")
longitude = center.get("longitude")
radius = area.get("radius")
area_type = area.get("areaType")

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