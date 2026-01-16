from rest_framework import serializers
from django.contrib.auth.models import User
from .models import WalletTransaction


# -------- AUTH --------
class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


# -------- ORDER --------
class OrderCreateSerializer(serializers.Serializer):
    order_id = serializers.CharField()
    total_price = serializers.FloatField()


# -------- BONUS (manual) --------
class AddBonusSerializer(serializers.Serializer):
    amount = serializers.FloatField()


# -------- WALLET HISTORY --------
class WalletTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletTransaction
        fields = [
            'id',
            'amount',
            'type',
            'reference_id',
            'created_at',
        ]
