import http.client

conn = http.client.HTTPSConnection("network-as-code.p-eu.rapidapi.com")

payload = "{\"device\":{\"phoneNumber\":\"+99999991001\",\"ipv4Address\":{\"publicAddress\":\"233.252.0.2\",\"privateAddress\":\"192.0.2.25\",\"publicPort\":80}},\"applicationServer\":{\"ipv4Address\":\"8.8.8.8\"},\"qosProfile\":\"DOWNLINK_M_UPLINK_L\",\"duration\":60}"

headers = {
    'x-rapidapi-key': "864f514522mshdac47d9f9f1b2a3p1f5397jsndef6161fc39b",
    'x-rapidapi-host': "network-as-code.nokia.rapidapi.com",
    'Content-Type': "application/json"
}

conn.request("POST", "/quality-on-demand/v1/sessions", payload, headers)

res = conn.getresponse()
data = res.read()

print(res.status, res.reason)
print(data.decode("utf-8"))