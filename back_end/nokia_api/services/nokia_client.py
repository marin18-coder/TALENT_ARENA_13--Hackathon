import httpx
from django.conf import settings

BASE = settings.RAPIDAPI_BASE


def _headers() -> dict:
    """
    Build required HTTP headers for Nokia Network-as-Code APIs via RapidAPI.
    """
    return {
        "x-rapidapi-key": settings.RAPIDAPI_KEY,
        "x-rapidapi-host": settings.RAPIDAPI_HOST,
        "Content-Type": "application/json",
    }


def post(path: str, payload: dict) -> dict:
    """
    Perform a synchronous POST request to a Nokia Network-as-Code endpoint.

    Centralizes:
    - Base URL construction
    - RapidAPI authentication headers
    - JSON serialization
    - Error normalization

    Args:
        path (str): Endpoint path.
        payload (dict): JSON body.

    Returns:
        dict:
            - On success → parsed JSON
            - On error (HTTP >= 400) →
              {"error": True, "status": <code>, "data": <json_or_raw>}
    """

    url = f"https://{BASE}{path}"

    try:
        with httpx.Client(timeout=20) as client:
            response = client.post(
                url,
                json=payload,
                headers=_headers(),
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

    except httpx.RequestError as e:
        return {
            "error": True,
            "status": 0,
            "data": {"message": f"Request failed: {str(e)}"},
        }