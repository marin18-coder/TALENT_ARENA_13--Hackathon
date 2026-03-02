import urllib.parse

CLIENT_ID = "TU_CLIENT_ID"
REDIRECT_URI = "https://tu-servidor.com/callback"  # tiene que estar configurado

params = {
    "response_type": "code",
    "client_id": CLIENT_ID,
    "redirect_uri": REDIRECT_URI,
    "scope": "number-verification",
    "state": "12345"
}

url = "https://network-as-code.p-eu.rapidapi.com/oauth2/v1/auth/authorize?" + urllib.parse.urlencode(params)

print(url)