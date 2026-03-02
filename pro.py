import http.client

RAPIDAPI_KEY = "TU_API_KEY"
HOST = "network-as-code.p-eu.rapidapi.com"

headers = {
    'x-rapidapi-key': "6b5cf197c0mshe27c521aaca32e8p1ac9aejsndc736cfb17f7",
    'x-rapidapi-host': "network-as-code.nokia.rapidapi.com",
    'Content-Type': "application/json"
}

phone_number = "+99999991000"

# ---------- SIM SWAP ----------

conn_sim = http.client.HTTPSConnection(HOST)

payload_sim = f'{{"phoneNumber":"{phone_number}","maxAge":240}}'

conn_sim.request(
    "POST",
    "/passthrough/camara/v1/sim-swap/sim-swap/v0/check",
    payload_sim,
    headers
)

res_sim = conn_sim.getresponse()
data_sim = res_sim.read()

print("SIM SWAP RESPONSE:")
print(data_sim.decode("utf-8"))


# ---------- DEVICE SWAP ----------

conn_device = http.client.HTTPSConnection(HOST)

payload_device = f'{{"phoneNumber":"{phone_number}","maxAge":120}}'

conn_device.request(
    "POST",
    "/passthrough/camara/v1/device-swap/device-swap/v1/check",
    payload_device,
    headers
)

res_device = conn_device.getresponse()
data_device = res_device.read()

print("\nDEVICE SWAP RESPONSE:")
print(data_device.decode("utf-8"))