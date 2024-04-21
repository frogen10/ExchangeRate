from rest_framework import serializers

from .models import Exchange

class ExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        read_only_fields = (
            "createdOn",
            "modifiedOn"
        ),
        fields =(
            "id",
            "name",
            "midValue",
            "bidValue",
            "askValue",
            "date",
            "currency"
        )