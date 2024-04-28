from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Client

class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        read_only_fields = (
            "created_at",
            "created_by",
        ),
        fields = (
            "id",
            "number",
            "first_name",
            "last_name",
            "address1",
            "address2",
            "zipcode",
            "place",
            "country",
            "default_currency"
        )
