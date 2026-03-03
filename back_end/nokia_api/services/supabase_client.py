from supabase import create_client, Client
from django.conf import settings


class SupabaseService:
    """
    Service layer responsible for interacting with Supabase.

    Handles:
    - Client initialization
    - Inserts
    - Reads
    - Table-level operations

    Does NOT contain business logic.
    """

    def __init__(self) -> None:
        self.client: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_SERVICE_KEY
        )

    # -----------------------------
    # LOCATION
    # -----------------------------

    def insert_location(self, phone_number: str, location_data: dict) -> None:
        area = location_data.get("area", {}) or {}
        center = area.get("center", {}) or {}

        payload = {
            "phone_number": phone_number,
            "latitude": center.get("latitude"),
            "longitude": center.get("longitude"),
            "accuracy": location_data.get("accuracy"),
            "location_timestamp": location_data.get("timestamp"),
            "raw_response": location_data,
        }

        self.client.table("location_history").insert(payload).execute()

    # -----------------------------
    # SIM SWAP
    # -----------------------------

    def insert_sim_swap(self, phone_number: str, last_date: str, raw_data: dict) -> None:

        payload = {
            "phone_number": phone_number,
            "swapped": True,
            "last_sim_swap_date": last_date,
            "raw_response": raw_data,
        }

        self.client.table("sim_swap_history").insert(payload).execute()

    def get_last_sim_swap(self, phone_number: str):
        return (
            self.client
            .table("sim_swap_history")
            .select("last_sim_swap_date")
            .eq("phone_number", phone_number)
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )