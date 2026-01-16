from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from .models import LoyaltyCard

User = get_user_model()


@receiver(post_save, sender=User)
def create_loyalty_card(sender, instance, created, **kwargs):
    if created:
        start = timezone.now()
        LoyaltyCard.objects.create(
            user=instance,
            cycle_start=start,
            cycle_end=start + timedelta(days=60)
        )
