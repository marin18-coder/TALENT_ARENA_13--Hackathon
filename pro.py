import http.client
import json

RAPIDAPI_KEY = "6b5cf197c0mshe27c521aaca32e8p1ac9aejsndc736cfb17f7"
HOST = "network-as-code.p-eu.rapidapi.com"

headers = {
    'x-rapidapi-key': "6b5cf197c0mshe27c521aaca32e8p1ac9aejsndc736cfb17f7",
    'x-rapidapi-host': "network-as-code.nokia.rapidapi.com",
    'Content-Type': "application/json"
}

phone_number = "+99999991000"

# ---------- SIM SWAP CHECK ----------

conn_sim = http.client.HTTPSConnection(HOST)

payload_sim_check = json.dumps({
    "phoneNumber": phone_number,
    "maxAge": 240
})

conn_sim.request(
    "POST",
    "/passthrough/camara/v1/sim-swap/sim-swap/v0/check",
    payload_sim_check,
    headers
)

res_sim = conn_sim.getresponse()
data_sim = json.loads(res_sim.read().decode("utf-8"))

print("SIM SWAP CHECK:")
print(data_sim)

# Si swapped es true → recuperar fecha
if data_sim.get("swapped"):

    conn_sim_retrieve = http.client.HTTPSConnection(HOST)

    payload_sim_retrieve = json.dumps({
        "phoneNumber": phone_number
    })

    conn_sim_retrieve.request(
        "POST",
        "/passthrough/camara/v1/sim-swap/sim-swap/v0/retrieve-date",
        payload_sim_retrieve,
        headers
    )

    res_sim_date = conn_sim_retrieve.getresponse()
    data_sim_date = json.loads(res_sim_date.read().decode("utf-8"))

    print("SIM SWAP LAST DATE:")
    print(data_sim_date)


# ---------- DEVICE SWAP CHECK ----------

conn_device = http.client.HTTPSConnection(HOST)

payload_device_check = json.dumps({
    "phoneNumber": phone_number,
    "maxAge": 120
})

conn_device.request(
    "POST",
    "/passthrough/camara/v1/device-swap/device-swap/v1/check",
    payload_device_check,
    headers
)

res_device = conn_device.getresponse()
data_device = json.loads(res_device.read().decode("utf-8"))

print("\nDEVICE SWAP CHECK:")
print(data_device)

# Si swapped es true → recuperar fecha
if data_device.get("swapped"):

    conn_device_retrieve = http.client.HTTPSConnection(HOST)

    payload_device_retrieve = json.dumps({
        "phoneNumber": phone_number
    })

    conn_device_retrieve.request(
        "POST",
        "/passthrough/camara/v1/device-swap/device-swap/v1/retrieve-date",
        payload_device_retrieve,
        headers
    )

    res_device_date = conn_device_retrieve.getresponse()
    data_device_date = json.loads(res_device_date.read().decode("utf-8"))

    print("DEVICE SWAP LAST DATE:")
    print(data_device_date)