import httpx
from django.conf import settings

BASE = settings.RAPIDAPI_BASE

def _headers() -> dict:
    """
    Build the required HTTP headers for Nokia Network-as-Code APIs via RapidAPI.

    Returns:
        dict: Headers including authentication and content type.
    """
    return {
        "x-rapidapi-key": settings.RAPIDAPI_KEY,
        "x-rapidapi-host": settings.RAPIDAPI_HOST,
        "Content-Type": "application/json",
    }


async def post(path: str, payload: dict) -> dict:
    """
    Perform an asynchronous POST request to a Nokia Network-as-Code endpoint.

    This function centralizes:
    - Base URL construction
    - Header injection (authentication via RapidAPI)
    - JSON serialization
    - Error handling normalization

    Args:
        path (str): API endpoint path (e.g. '/passthrough/camara/v1/sim-swap/...').
        payload (dict): JSON payload to be sent in the request body.

    Returns:
        dict:
            - On success: Parsed JSON response from Nokia API.
            - On error (HTTP >= 400): 
                {"error": True, "status": <status_code>, "data": <parsed_json_or_raw_text>}
    """

    url = f"https://{BASE}{path}"

    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.post(
            url,
            json=payload,
            headers=_headers()
        )

        try:
            data = response.json()
        except Exception:
            data = {"raw": response.text}

        if response.status_code >= 400:
            return {
                "error": True,
                "status": response.status_code,
                "data": data,
            }

        return data