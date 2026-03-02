from supabase import create_client, Client
from number_recycling import check_number_recycling
# -------- CONFIG --------

SUPABASE_URL = "https://cyvyilelgipfcrwzssmv.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN5dnlpbGVsZ2lwZmNyd3pzc212Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MjQ1MDA1NSwiZXhwIjoyMDg4MDI2MDU1fQ.u4vj6cDwyTHTTEAjUNDUcymCx0LK4VQ6n8zrvouNZFQ"

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

print("\nÚltimos 20 Device Swap Dates:")
for row in device_swap_response.data:
    print(row["last_device_swap_date"])


# ---------- LOCATION HISTORY ----------

location_response = (
    supabase
    .table("location_history")
    .select("latitude, longitude")
    .order("created_at", desc=True)
    .limit(20)
    .execute()
)

print("\nÚltimas 20 Ubicaciones:")
for row in location_response.data:
    print(f"Lat: {row['latitude']} | Lon: {row['longitude']}")


# ---------- SIM SWAP HISTORY ----------

sim_swap_response = (
    supabase
    .table("sim_swap_history")
    .select("last_sim_swap_date")
    .order("created_at", desc=True)
    .limit(20)
    .execute()
)

print("\nÚltimos 20 SIM Swap Dates:")
for row in sim_swap_response.data:
    print(row["last_sim_swap_date"])

# ----------  NUMBER RECYCLED ----------

phone = "+99999991000"
date = "2024-10-31"

result = check_number_recycling(phone, date)

print("\nResultado Number Recycling:")
print(result)