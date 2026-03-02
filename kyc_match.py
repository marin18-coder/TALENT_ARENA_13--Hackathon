import http.client
import json

RAPIDAPI_KEY = "TU_RAPIDAPI_KEY"
HOST = "network-as-code.p-eu.rapidapi.com"

def kyc_match(data_payload):

    conn = http.client.HTTPSConnection(HOST)

    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': "network-as-code.nokia.rapidapi.com",
        'Content-Type': "application/json; charset=utf-8",
        'x-correlator': "b4333c46-49c0-4f62-80d7-f0ef930f1c46"
    }

    payload = json.dumps(data_payload)

    conn.request(
        "POST",
        "/passthrough/camara/v1/kyc-match/kyc-match/v0.3/match",
        payload.encode("utf-8"),
        headers
    )

    res = conn.getresponse()
    raw = res.read().decode("utf-8")

    if res.status != 200:
        return {"error": raw}

    return json.loads(raw) 