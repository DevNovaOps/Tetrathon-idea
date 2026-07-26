"""
Transaction models for digital transaction import and classification.
"""
import uuid
from django.db import models
from django.conf import settings


PAYMENT_METHOD_CHOICES = [
    ('upi', 'UPI'),
    ('debit_card', 'Debit Card'),
    ('credit_card', 'Credit Card'),
    ('bank_transfer', 'Bank Transfer'),
    ('cash', 'Cash'),
    ('wallet', 'Wallet'),
]

SOURCE_CHOICES = [
    ('manual', 'Manual Entry'),
    ('csv_import', 'CSV Import'),
    ('upi_sync', 'UPI Sync'),
    ('card_sync', 'Card Sync'),
    ('bank_sync', 'Bank Sync'),
    ('demo', 'Synthetic Demo Data'),
]

CATEGORY_CHOICES = [
    ('salary', 'Salary'),
    ('freelance', 'Freelance Income'),
    ('investment_income', 'Investment Income'),
    ('refund', 'Refund'),
    ('other_income', 'Other Income'),
    ('groceries', 'Groceries'),
    ('food', 'Food & Dining'),
    ('transport', 'Transport'),
    ('entertainment', 'Entertainment'),
    ('shopping', 'Shopping'),
    ('utilities', 'Utilities'),
    ('health', 'Health & Medical'),
    ('education', 'Education'),
    ('investment', 'Investment'),
    ('rent', 'Rent'),
    ('emi', 'EMI / Loan'),
    ('insurance', 'Insurance'),
    ('travel', 'Travel'),
    ('personal_care', 'Personal Care'),
    ('subscriptions', 'Subscriptions'),
    ('charity', 'Charity / Donations'),
    ('transfer', 'Transfer'),
    ('other', 'Other'),
]


class Transaction(models.Model):
    """
    Stores every financial transaction for a user.
    Supports auto-classification with manual correction.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transactions'
    )

    amount = models.DecimalField(max_digits=15, decimal_places=2)
    merchant = models.CharField(max_length=200, blank=True, default='')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    original_category = models.CharField(max_length=50, blank=True, default='')
    date = models.DateField(db_index=True)
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD_CHOICES, default='upi')
    location = models.CharField(max_length=200, blank=True, default='')
    description = models.TextField(blank=True, default='')
    source = models.CharField(max_length=30, choices=SOURCE_CHOICES, default='manual')
    is_income = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'transactions'
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['user', 'date']),
            models.Index(fields=['user', 'category']),
            models.Index(fields=['user', 'is_income']),
        ]

    def __str__(self):
        direction = '+' if self.is_income else '-'
        return f"{direction}₹{self.amount} {self.merchant or self.category} ({self.date})"
