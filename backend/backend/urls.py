# backend/urls.py
from django.contrib import admin
from django.urls import path, include
from routing import Router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(Router)),
]