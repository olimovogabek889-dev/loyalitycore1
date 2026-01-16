from django.contrib.auth.models import User
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from .models import LoyaltyCard, WalletTransaction
from .services import add_bonus
from .serializers import (
    RegisterSerializer,
    OrderCreateSerializer,
    AddBonusSerializer,
    WalletTransactionSerializer,
)


# ================= AUTH =================
class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "User already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        User.objects.create_user(username=username, password=password)
        return Response({"message": "Registered"}, status=status.HTTP_201_CREATED)


# ================= LOYALTY =================
class MyLoyaltyCardView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        card = LoyaltyCard.objects.get(user=request.user)
        return Response({
            "balance": card.current_balance,
            "cycle_start": card.cycle_start,
            "cycle_end": card.cycle_end,
            "cycle_number": card.cycle_number,
        })


class AddBonusView(GenericAPIView):
    serializer_class = AddBonusSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data['amount']
        card = LoyaltyCard.objects.get(user=request.user)

        add_bonus(card, amount, tx_type='manual')

        return Response({
            "message": "Bonus added",
            "new_balance": card.current_balance
        })


class WalletHistoryView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = WalletTransaction.objects.filter(user=request.user)
        serializer = WalletTransactionSerializer(qs, many=True)
        return Response(serializer.data)


# ================= ORDERS =================
class CreateOrderView(GenericAPIView):
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order_id = serializer.validated_data['order_id']
        total_price = serializer.validated_data['total_price']

        bonus = total_price * 0.05
        card = LoyaltyCard.objects.get(user=request.user)

        add_bonus(card, bonus, tx_type='order', reference_id=order_id)

        return Response({
            "order_id": order_id,
            "bonus_added": bonus,
            "new_balance": card.current_balance
        })
