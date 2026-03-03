from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

from .nokia_client import post

# ---- Endpoints (avoid typos) ----
LOCATION_RETRIEVE = "/location-retrieval/v0/retrieve"

SIM_SWAP_CHECK = "/passthrough/camara/v1/sim-swap/sim-swap/v0/check"
SIM_SWAP_DATE = "/passthrough/camara/v1/sim-swap/sim-swap/v0/retrieve-date"

DEVICE_SWAP_CHECK = "/passthrough/camara/v1/device-swap/device-swap/v1/check"
DEVICE_SWAP_DATE = "/passthrough/camara/v1/device-swap/device-swap/v1/retrieve-date"

NUMBER_RECYCLING_CHECK = "/passthrough/camara/v1/number-recycling/number-recycling/v0.2/check"


def _ok(data: dict) -> bool:
    """Return True if Nokia client response is not an error envelope."""
    return isinstance(data, dict) and not data.get("error", False)


async def retrieve_location(phone_number: str, max_age: int = 60) -> dict:
    """
    Retrieve last known device location using Nokia location retrieval API.
    """
    payload = {"device": {"phoneNumber": phone_number}, "maxAge": max_age}
    return await post(LOCATION_RETRIEVE, payload)


async def sim_swap_check(phone_number: str, max_age: int = 240) -> dict:
    """
    Check whether a SIM swap occurred within maxAge minutes.
    """
    return await post(SIM_SWAP_CHECK, {"phoneNumber": phone_number, "maxAge": max_age})


async def sim_swap_retrieve_date(phone_number: str) -> dict:
    """
    Retrieve the last SIM swap date.
    """
    return await post(SIM_SWAP_DATE, {"phoneNumber": phone_number})


async def device_swap_check(phone_number: str, max_age: int = 120) -> dict:
    """
    Check whether a device swap occurred within maxAge minutes.
    """
    return await post(DEVICE_SWAP_CHECK, {"phoneNumber": phone_number, "maxAge": max_age})


async def device_swap_retrieve_date(phone_number: str) -> dict:
    """
    Retrieve the last device swap date.
    """
    return await post(DEVICE_SWAP_DATE, {"phoneNumber": phone_number})


async def number_recycling_check(phone_number: str, years_back: int = 1) -> dict:
    """
    Check whether the number was recycled since a specified date.
    """
    specified_date = (
        datetime.now(timezone.utc) - timedelta(days=365 * years_back)
    ).strftime("%Y-%m-%d")

    return await post(
        NUMBER_RECYCLING_CHECK,
        {"phoneNumber": phone_number, "specifiedDate": specified_date},
    )


async def run_full_scan(phone_number: str) -> dict:
    """
    Run a full Nokia scan and return a stable, frontend-friendly payload.

    Returns:
        dict with keys:
            location, simSwap, simSwapDate, deviceSwap, deviceSwapDate, numberRecycling
            Each key is always present (value can be None if an API call failed).
    """
    location = await retrieve_location(phone_number)
    sim = await sim_swap_check(phone_number)
    dev = await device_swap_check(phone_number)
    rec = await number_recycling_check(phone_number)

    sim_date = None
    if _ok(sim) and sim.get("swapped"):
        sim_date = await sim_swap_retrieve_date(phone_number)

    dev_date = None
    if _ok(dev) and dev.get("swapped"):
        dev_date = await device_swap_retrieve_date(phone_number)

    return {
        "location": location if _ok(location) else None,
        "simSwap": sim if _ok(sim) else None,
        "simSwapDate": sim_date if _ok(sim_date or {}) else sim_date,  # keep None or dict
        "deviceSwap": dev if _ok(dev) else None,
        "deviceSwapDate": dev_date if _ok(dev_date or {}) else dev_date,
        "numberRecycling": rec if _ok(rec) else None,
    }