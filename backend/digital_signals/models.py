"""
Digital Signals — Non-Traditional Financial Signal Models.
Stores user-reported digital payment and utility bill behaviours.
"""
import uuid
from django.db import models
from django.conf import settings


BILL_FREQUENCY_CHOICES = [
    ('always_on_time', 'Always On Time'),
    ('occasionally_late', 'Occasionally Late'),
    ('frequently_late', 'Frequently Late'),
    ('no_bills', 'No Bills'),
]

RECHARGE_FREQUENCY_CHOICES = [
    ('monthly', 'Monthly'),
    ('quarterly', 'Quarterly'),
    ('irregular', 'Irregular'),
    ('prepaid', 'Prepaid Auto-Recharge'),
]

BROADBAND_PAYMENT_CHOICES = [
    ('always_on_time', 'Always On Time'),
    ('occasionally_late', 'Occasionally Late'),
    ('no_broadband', 'No Broadband'),
]

DIGITAL_TX_FREQUENCY_CHOICES = [
    ('multiple_daily', 'Multiple Times a Day'),
    ('daily', 'Daily'),
    ('weekly', 'Few Times a Week'),
    ('rarely', 'Rarely'),
    ('never', 'Never'),
]

SHOPPING_FREQUENCY_CHOICES = [
    ('weekly', 'Weekly'),
    ('biweekly', 'Bi-weekly'),
    ('monthly', 'Monthly'),
    ('rarely', 'Rarely'),
]

REGULARITY_CHOICES = [
    ('excellent', 'Excellent'),
    ('good', 'Good'),
    ('average', 'Average'),
    ('poor', 'Poor'),
]

SPENDING_BEHAVIOUR_CHOICES = [
    ('high', 'High'),
    ('moderate', 'Moderate'),
    ('low', 'Low'),
    ('minimal', 'Minimal'),
]


class DigitalSignalProfile(models.Model):
    """
    Stores non-traditional digital financial signals per user.
    These feed into the Credit Score Engine as additional scoring dimensions.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='digital_signals'
    )

    # Utility bill payments
    electricity_bill_frequency = models.CharField(
        max_length=30, choices=BILL_FREQUENCY_CHOICES, default='always_on_time'
    )
    water_bill_frequency = models.CharField(
        max_length=30, choices=BILL_FREQUENCY_CHOICES, default='always_on_time'
    )
    gas_bill_frequency = models.CharField(
        max_length=30, choices=BILL_FREQUENCY_CHOICES, default='no_bills'
    )

    # Telecom & broadband
    mobile_recharge_frequency = models.CharField(
        max_length=30, choices=RECHARGE_FREQUENCY_CHOICES, default='monthly'
    )
    broadband_payment = models.CharField(
        max_length=30, choices=BROADBAND_PAYMENT_CHOICES, default='always_on_time'
    )

    # Digital payment frequency
    upi_transaction_frequency = models.CharField(
        max_length=30, choices=DIGITAL_TX_FREQUENCY_CHOICES, default='daily'
    )
    card_transaction_frequency = models.CharField(
        max_length=30, choices=DIGITAL_TX_FREQUENCY_CHOICES, default='weekly'
    )

    # Spending patterns
    shopping_frequency = models.CharField(
        max_length=30, choices=SHOPPING_FREQUENCY_CHOICES, default='monthly'
    )
    utility_payment_regularity = models.CharField(
        max_length=30, choices=REGULARITY_CHOICES, default='good'
    )
    online_spending_behaviour = models.CharField(
        max_length=30, choices=SPENDING_BEHAVIOUR_CHOICES, default='moderate'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'digital_signal_profiles'
        verbose_name = 'Digital Signal Profile'

    def __str__(self):
        return f"Digital Signals for {self.user.email}"
