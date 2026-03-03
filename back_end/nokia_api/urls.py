from django.urls import path
from . import views

urlpatterns = [
    path("health/", views.health),
    path("location/", views.location_view),
    path("sim-swap/", views.sim_swap_check_view),
    path("device-swap/", views.device_swap_check_view),
    path("number-recycling/", views.number_recycling_view),
    path("full-scan/", views.full_scan_view),
    path("persist-location/", views.persist_location_view),
]