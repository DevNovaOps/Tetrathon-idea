"""UserProfile model — stores all onboarding data separate from User."""
from django.conf import settings
from django.db import models

from .constants import (
    BILL_PAYMENT_CHOICES,
    EMERGENCY_FUND_CHOICES,
    EXISTING_LOAN_CHOICES,
    FINANCIAL_GOAL_CHOICES,
    GENDER_CHOICES,
    INVESTMENT_DURATION_CHOICES,
    INVESTMENT_EXPERIENCE_CHOICES,
    LANGUAGE_CHOICES,
    RISK_PREFERENCE_CHOICES,
    UPI_USAGE_CHOICES,
)


class UserProfile(models.Model):
    """
    One-to-one extension of User for onboarding data.
    Designed for future module integration (credit score, AI, etc.).
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
        primary_key=True,
    )

    # ── Step 1: Personal Information ──────────────────────────────────
    full_name = models.CharField(max_length=150, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=30, choices=GENDER_CHOICES, blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    preferred_language = models.CharField(
        max_length=30, choices=LANGUAGE_CHOICES, blank=True,
    )

    # ── Step 2: Financial Profile ─────────────────────────────────────
    monthly_income = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    monthly_expenses = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    savings = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    existing_loans = models.CharField(
        max_length=50, choices=EXISTING_LOAN_CHOICES, blank=True,
    )
    upi_usage = models.CharField(
        max_length=50, choices=UPI_USAGE_CHOICES, blank=True,
    )
    bill_payment_habit = models.CharField(
        max_length=50, choices=BILL_PAYMENT_CHOICES, blank=True,
    )

    # ── Step 3: Investment Profile ────────────────────────────────────
    investment_experience = models.CharField(
        max_length=50, choices=INVESTMENT_EXPERIENCE_CHOICES, blank=True,
    )
    emergency_fund = models.CharField(
        max_length=50, choices=EMERGENCY_FUND_CHOICES, blank=True,
    )
    monthly_investment_budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    financial_goal = models.CharField(
        max_length=50, choices=FINANCIAL_GOAL_CHOICES, blank=True,
    )
    risk_preference = models.CharField(
        max_length=50, choices=RISK_PREFERENCE_CHOICES, blank=True,
    )
    investment_duration = models.CharField(
        max_length=50, choices=INVESTMENT_DURATION_CHOICES, blank=True,
    )

    # ── Future Architecture (Dashboard/AI/Credit) ─────────────────────
    credit_score = models.PositiveIntegerField(null=True, blank=True)
    total_assets = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    risk_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    # ── Progress Tracking ─────────────────────────────────────────────
    current_step = models.PositiveIntegerField(default=1)
    step1_completed = models.BooleanField(default=False)
    step2_completed = models.BooleanField(default=False)
    step3_completed = models.BooleanField(default=False)
    onboarding_completed = models.BooleanField(default=False)

    # ── Timestamps ────────────────────────────────────────────────────
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_profiles'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self) -> str:
        return f'Profile of {self.user.email}'
