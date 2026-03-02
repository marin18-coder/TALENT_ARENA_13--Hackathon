import http.client

conn = http.client.HTTPSConnection("network-as-code.p-eu.rapidapi.com")

payload = "{\"phoneNumber\":\"+99999991000\",\"idDocument\":\"66666666q\",\"name\":\"Federica Sanchez Arjona\",\"givenName\":\"Federica\",\"familyName\":\"Sanchez Arjona\",\"nameKanaHankaku\":\"federica\",\"nameKanaZenkaku\":\"Ｆｅｄｅｒｉｃａ\",\"middleNames\":\"Sanchez\",\"familyNameAtBirth\":\"YYYY\",\"address\":\"Tokyo-to Chiyoda-ku Iidabashi 3-10-10\",\"streetName\":\"Nicolas Salmeron\",\"streetNumber\":\"4\",\"postalCode\":\"1028460\",\"region\":\"Tokyo\",\"locality\":\"ZZZZ\",\"country\":\"JP\",\"houseNumberExtension\":\"VVVV\",\"birthdate\":\"1978-08-22\",\"email\":\"abc@example.com\",\"gender\":\"OTHER\"}"

headers = {
    'x-rapidapi-key': "864f514522mshdac47d9f9f1b2a3p1f5397jsndef6161fc39b",
    'x-rapidapi-host': "network-as-code.nokia.rapidapi.com",
    'Content-Type': "application/json; charset=utf-8",
    'x-correlator': "b4333c46-49c0-4f62-80d7-f0ef930f1c46"
}

# 👇 SOLO ESTE CAMBIO
conn.request(
    "POST",
    "/passthrough/camara/v1/kyc-match/kyc-match/v0.3/match",
    payload.encode("utf-8"),
    headers
)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))