import requests
import settings as s

class DeviceStatus:
    """Client to retrieve device status from Device Status Network-as-Code API."""

    BASE_URL = ("https://network-as-code.p-eu.rapidapi.com/device-status/v0/connectivity")

    def __init__(self, phone_number: str = "+99999991000", api_key: str = None):
        self.phone_number = phone_number
        self.api_key = api_key

        self.headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "network-as-code.nokia.rapidapi.com",
            "Content-Type": "application/json",
            "x-correlator": "b4333c46-49c0-4f62-80d7-f0ef930f1c46",
        }

    def get_device_status(self) -> bool | None:
        """
            Fetch device status.

            Returns:
                bool: True if device is available, False if not, None if an error occurs.
        """

        payload = {"device": {"phoneNumber": self.phone_number}}

        try:
            response = requests.post(self.BASE_URL, json=payload, headers=self.headers, timeout=10)
            data = response.json()
            connectivity = data.get("connectivityStatus", "")
            if connectivity in ["CONNECTED_SMS", "CONNECTED_DATA"]:
                return True
            elif connectivity in ["NOT_CONNECTED", ""]:
                return False
            return None

        except requests.RequestException as exc:
            print(f"Request failed: {exc}")
            return None
        except ValueError:
            print("Invalid JSON response")
            return None
        
        

