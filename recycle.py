import http.client
import json
from datetime import datetime, timedelta

RAPIDAPI_KEY = "TU_API_KEY"
HOST = "network-as-code.p-eu.rapidapi.com"

headers = {
    'x-rapidapi-key': "6b5cf197c0mshe27c521aaca32e8p1ac9aejsndc736cfb17f7",
    'x-rapidapi-host': "network-as-code.nokia.rapidapi.com",
    'Content-Type': "application/json"
}

phone_number = "+99999991000"

# Periodos en días aproximados
periods = {
    "1 mes": 30,
    "6 meses": 180,
    "1 año": 365,
    "3 años": 365 * 3,
    "5 años": 365 * 5,
    "10 años": 365 * 10
}

for label, days in periods.items():

    specified_date = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d")

    payload = json.dumps({
        "phoneNumber": phone_number,
        "specifiedDate": specified_date
    })

    conn = http.client.HTTPSConnection(HOST)

    conn.request(
        "POST",
        "/passthrough/camara/v1/number-recycling/number-recycling/v0.2/check",
        payload,
        headers
    )

    res = conn.getresponse()
    data = res.read()

    print(f"\nPeriodo: {label}")
    print(f"Desde: {specified_date}")
    print("Respuesta API:")
    print(data.decode("utf-8"))