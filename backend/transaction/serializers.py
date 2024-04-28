from rest_framework import serializers

from .models import Balance, Transaction

class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        read_only_fields = (
            "created_at",
            "created_by",
        ),
        fields =(
            "id",
            "value",
            "currency"
        )

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        read_only_fields = (
            "created_by", 
        ),
        fields =(
            "id",
            "type",
            "value",
            "from_currency",
            "to_currency",
            "created_at",
        )