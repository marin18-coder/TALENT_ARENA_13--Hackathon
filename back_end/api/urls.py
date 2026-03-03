"""
URL configuration for api project.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Nokia API endpoints
    path('api/nokia/', include('nokia_api.urls')),
]