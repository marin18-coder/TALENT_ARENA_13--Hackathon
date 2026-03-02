from supabase import create_client, Client

# -------- CONFIG --------

SUPABASE_URL = "https://TU_PROYECTO.supabase.co"
SUPABASE_KEY = "TU_SUPABASE_SERVICE_ROLE_KEY"

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