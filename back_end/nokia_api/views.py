from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import PhoneSerializer
from .services.analyzers import (
    retrieve_location,
    sim_swap_check,
    sim_swap_retrieve_date,
    device_swap_check,
    device_swap_retrieve_date,
    number_recycling_check,
    run_full_scan,
)
from .services.supabase_client import SupabaseService


# ---------------------------------
# Health
# ---------------------------------

@api_view(["GET"])
def health(request):
    return Response(
        {"ok": True, "service": "nokia_api"},
        status=status.HTTP_200_OK,
    )


# ---------------------------------
# Location
# ---------------------------------

@api_view(["POST"])
async def location_view(request):
    serializer = PhoneSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    phone = serializer.validated_data["phoneNumber"]

    data = await retrieve_location(phone)

    return Response(
        {"ok": True, "phoneNumber": phone, "data": data},
        status=status.HTTP_200_OK,
    )


# ---------------------------------
# SIM SWAP CHECK
# ---------------------------------

@api_view(["POST"])
async def sim_swap_check_view(request):
    serializer = PhoneSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    phone = serializer.validated_data["phoneNumber"]
    max_age = request.data.get("maxAge", 240)

    data = await sim_swap_check(phone, max_age=int(max_age))

    return Response({"ok": True, "data": data})


# ---------------------------------
# DEVICE SWAP CHECK
# ---------------------------------

@api_view(["POST"])
async def device_swap_check_view(request):
    serializer = PhoneSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    phone = serializer.validated_data["phoneNumber"]
    max_age = request.data.get("maxAge", 120)

    data = await device_swap_check(phone, max_age=int(max_age))

    return Response({"ok": True, "data": data})


# ---------------------------------
# NUMBER RECYCLING
# ---------------------------------

@api_view(["POST"])
async def number_recycling_view(request):
    serializer = PhoneSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    phone = serializer.validated_data["phoneNumber"]
    years_back = request.data.get("yearsBack", 1)

    data = await number_recycling_check(phone, years_back=int(years_back))

    return Response({"ok": True, "data": data})


# ---------------------------------
# FULL SCAN
# ---------------------------------

@api_view(["POST"])
async def full_scan_view(request):
    serializer = PhoneSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    phone = serializer.validated_data["phoneNumber"]
    scan = await run_full_scan(phone)

    return Response(
        {"ok": True, "phoneNumber": phone, "scan": scan},
        status=status.HTTP_200_OK,
    )


# ---------------------------------
# Persist Location (optional)
# ---------------------------------

@api_view(["POST"])
async def persist_location_view(request):
    serializer = PhoneSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    phone = serializer.validated_data["phoneNumber"]

    location = await retrieve_location(phone)

    try:
        sb = SupabaseService()
        sb.insert_location(phone, location)

        return Response(
            {"ok": True, "saved": True, "data": location},
            status=status.HTTP_200_OK,
        )

    except Exception as e:
        return Response(
            {"ok": False, "error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )