"""
foodgram URL Configuration
"""
from django.contrib import admin
from django.urls import include, path

from recipes.views import *  # Test


urlpatterns = (
    path('admin/', admin.site.urls),
    path('', recipes_index),  # Test
    # Роутинг приложения api
    path('api/', include('api.urls', namespace='api')),
)
