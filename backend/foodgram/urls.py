"""
foodgram URL Configuration
"""
from django.contrib import admin
from django.urls import include, path


urlpatterns = (
    # Роутинг инструментов администрирования
    path("admin/", admin.site.urls),
    # Роутинг приложения api
    path("api/", include("api.urls", namespace="api")),
)
