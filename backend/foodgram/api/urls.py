"""
api URL Configuration
"""
from django.urls import include, path

from api.views import api_index


app_name = 'api'

urlpatterns = (
    path('', api_index),  # Test
    # Router
)
