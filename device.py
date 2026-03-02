import http.client
import json
import time
from datetime import datetime
from supabase import create_client, Client

# -------- CONFIG --------

RAPIDAPI_KEY = "6b5cf197c0mshe27c521aaca32e8p1ac9aejsndc736cfb17f7"
HOST = "network-as-code.p-eu.rapidapi.com"

SUPABASE_URL = "https://cyvyilelgipfcrwzssmv.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN5dnlpbGVsZ2lwZmNyd3pzc212Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MjQ1MDA1NSwiZXhwIjoyMDg4MDI2MDU1fQ.u4vj6cDwyTHTTEAjUNDUcymCx0LK4VQ6n8zrvouNZFQ"

CHECK_INTERVAL_SECONDS = 300  # cada 5 minutos

phone_number = "+99999991000"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

headers = {
    'x-rapidapi-key': RAPIDAPI_KEY,
    'x-rapidapi-host': "network-as-code.nokia.rapidapi.com",
    'Content-Type': "application/json"
}


def get_last_device_swap_date_from_api():
    conn = http.client.HTTPSConnection(HOST)

    payload = json.dumps({
        "phoneNumber": phone_number
    })

    conn.request(
        "POST",
        "/passthrough/camara/v1/device-swap/device-swap/v1/retrieve-date",
        payload,
        headers
    )

    res = conn.getresponse()
    raw = res.read().decode("utf-8")

    if res.status != 200:
        print("Error API:", raw)
        return None

    data = json.loads(raw)
    return data.get("lastDeviceSwapDate")


def get_last_saved_swap_from_db():
    response = (
        supabase
        .table("device_swap_history")
        .select("last_device_swap_date")
        .eq("phone_number", phone_number)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )

    if response.data and len(response.data) > 0:
        return response.data[0]["last_device_swap_date"]

    return None


def insert_new_swap(date_value):
    insert_data = {
        "phone_number": phone_number,
        "swapped": True,
        "last_device_swap_date": date_value,
        "max_age_minutes": None,
        "raw_response": {"lastDeviceSwapDate": date_value}
    }

    supabase.table("device_swap_history").insert(insert_data).execute()
    print("Nuevo swap guardado en BD:", date_value)


# -------- LOOP PRINCIPAL --------

while True:
    print("Comprobando device swap...")

    api_date = get_last_device_swap_date_from_api()

    if api_date is None:
        time.sleep(CHECK_INTERVAL_SECONDS)
        continue

    db_date = get_last_saved_swap_from_db()

    print("API date:", api_date)
    print("DB date:", db_date)

    if db_date != api_date:
        insert_new_swap(api_date)
    else:
        print("No hay cambios.")

    print("Esperando...\n")
    time.sleep(CHECK_INTERVAL_SECONDS)