from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

User = settings.AUTH_USER_MODEL


class LoyaltyCard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    cycle_start = models.DateTimeField()
    cycle_end = models.DateTimeField()
    cycle_days = models.PositiveIntegerField(default=60)
    cycle_number = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def start_new_cycle(self):
        self.cycle_start = timezone.now()
        self.cycle_end = self.cycle_start + timedelta(days=self.cycle_days)
        self.current_balance = 0
        self.cycle_number += 1
        self.save()

    def __str__(self):
        return f"{self.user} | balance={self.current_balance}"


class WalletTransaction(models.Model):
    TYPES = (
        ('order', 'Order Bonus'),
        ('manual', 'Manual Bonus'),
        ('expire', 'Expired'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=20, choices=TYPES)
    reference_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} | {self.type} | {self.amount}"
