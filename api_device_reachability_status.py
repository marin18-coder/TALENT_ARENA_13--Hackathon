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

