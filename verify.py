import http.client
import json

conn = http.client.HTTPSConnection("network-as-code.p-eu.rapidapi.com")

headers = {
    'x-rapidapi-key': "6b5cf197c0mshe27c521aaca32e8p1ac9aejsndc736cfb17f7",
    'x-rapidapi-host': "network-as-code.nokia.rapidapi.com"
}

conn.request(
    "GET",
    "/passthrough/camara/v1/nac-authorization-server/client-credentials",
    headers=headers
)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))