import http.client
import json

RAPIDAPI_KEY = "6b5cf197c0mshe27c521aaca32e8p1ac9aejsndc736cfb17f7"
HOST = "network-as-code.p-eu.rapidapi.com"

def check_number_recycling(phone_number, specified_date):

    conn = http.client.HTTPSConnection(HOST)

    payload = json.dumps({
        "phoneNumber": phone_number,
        "specifiedDate": specified_date
    })

    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': "network-as-code.nokia.rapidapi.com",
        'Content-Type': "application/json"
    }

    conn.request(
        "POST",
        "/passthrough/camara/v1/number-recycling/number-recycling/v0.2/check",
        payload,
        headers
    )

    res = conn.getresponse()
    raw_data = res.read().decode("utf-8")

    if res.status != 200:
        return {"error": raw_data}

    return json.loads(raw_data)