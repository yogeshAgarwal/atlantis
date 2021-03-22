# Django Library
from django.urls import path

# Local Library
from .views import (
    Registration,
    UpdateLocation,
    SearchLocation,
)

urlpatterns = [
    path(
        'register/',
        Registration.as_view(),
        name='register'),
    path(
        'api/<int:driver_id>/update-location/',
        UpdateLocation.as_view(),
        name='update-location'),
    path(
        'search-location/',
        SearchLocation.as_view(),
        name='search-location'),
]