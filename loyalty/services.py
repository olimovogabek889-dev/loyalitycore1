from decimal import Decimal
from django.utils import timezone
from .models import WalletTransaction


def add_bonus(card, amount, tx_type, reference_id=None):
    # amount ni Decimal ga o‘tkazamiz (ENG MUHIM)
    amount = Decimal(str(amount))

    # Cycle tugagan bo‘lsa
    if timezone.now() > card.cycle_end:
        if card.current_balance > 0:
            WalletTransaction.objects.create(
                user=card.user,
                amount=card.current_balance,
                type='expire'
            )
        card.start_new_cycle()

    # Bonus qo‘shish
    card.current_balance += amount
    card.save(update_fields=["current_balance", "updated_at"])

    WalletTransaction.objects.create(
        user=card.user,
        amount=amount,
        type=tx_type,
        reference_id=reference_id
    )

    return card
