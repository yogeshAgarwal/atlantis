# Django Library
from django.urls import path

# Local Library
from .views import (
    Assignment1
)

urlpatterns = [
    path(
        'generate-csv/',
        Assignment1.as_view(),
        name='generate-csv'),
]