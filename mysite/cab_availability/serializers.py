from rest_framework import serializers

# Own Library
from .models import CabDriver, CabPosition

# Local Library


class CabDriverSerializer(serializers.ModelSerializer):

    class Meta:
        model = CabDriver
        fields = "__all__"

