from rest_framework import serializers
from .chart import Chart
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

class ChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chart
        fields =(
            "labels",
            "values",
            "label",
            "color"
        )