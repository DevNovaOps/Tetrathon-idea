"""Serializers for onboarding steps — server-side validation."""
import re
from decimal import Decimal, InvalidOperation

from rest_framework import serializers

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
    valid_values,
)


def _choice_validator(choices, field_label: str):
    """Return a validator function for a choice field."""
    allowed = valid_values(choices)

    def validator(value):
        if value not in allowed:
            raise serializers.ValidationError(
                f'Invalid {field_label}. Allowed: {", ".join(sorted(allowed))}'
            )

    return validator


def _clean_currency(value: str) -> Decimal:
    """Strip currency symbols, commas, and suffixes, then convert to Decimal."""
    if not isinstance(value, str):
        return value
    # Remove everything except digits and decimal point
    cleaned = re.sub(r'[^\d.]', '', value)
    try:
        return Decimal(cleaned) if cleaned else None
    except InvalidOperation:
        raise serializers.ValidationError('Invalid currency format.')

def _format_currency(value, suffix='') -> str:
    """Format decimal back to frontend string format."""
    if value is None:
        return ""
    # Just format as integer with commas and ₹ symbol
    return f"₹{int(value):,}{suffix}"


class Step1Serializer(serializers.Serializer):
    """Step 1 — Personal Information."""

    full_name = serializers.CharField(max_length=150)
    age = serializers.IntegerField(min_value=13, max_value=120)
    gender = serializers.CharField(max_length=30)
    occupation = serializers.CharField(max_length=100)
    city = serializers.CharField(max_length=100)
    preferred_language = serializers.CharField(max_length=30)

    def validate_full_name(self, value: str) -> str:
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError('Full name must be at least 2 characters.')
        return value

    def validate_gender(self, value: str) -> str:
        _choice_validator(GENDER_CHOICES, 'gender')(value)
        return value

    def validate_occupation(self, value: str) -> str:
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError('Occupation must be at least 2 characters.')
        return value

    def validate_city(self, value: str) -> str:
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError('City must be at least 2 characters.')
        return value

    def validate_preferred_language(self, value: str) -> str:
        _choice_validator(LANGUAGE_CHOICES, 'language')(value)
        return value


class Step2Serializer(serializers.Serializer):
    """Step 2 — Financial Profile."""

    monthly_income = serializers.CharField(max_length=50)
    monthly_expenses = serializers.CharField(max_length=50)
    savings = serializers.CharField(max_length=50)
    existing_loans = serializers.CharField(max_length=50)
    upi_usage = serializers.CharField(max_length=50)
    bill_payment_habit = serializers.CharField(max_length=50)

    def validate_monthly_income(self, value: str) -> Decimal:
        value = value.strip()
        if not value:
            raise serializers.ValidationError('Monthly income is required.')
        val = _clean_currency(value)
        if val is None:
            raise serializers.ValidationError('Invalid currency format.')
        return val

    def validate_monthly_expenses(self, value: str) -> Decimal:
        value = value.strip()
        if not value:
            raise serializers.ValidationError('Monthly expenses is required.')
        val = _clean_currency(value)
        if val is None:
            raise serializers.ValidationError('Invalid currency format.')
        return val

    def validate_savings(self, value: str) -> Decimal:
        value = value.strip()
        if not value:
            raise serializers.ValidationError('Current savings is required.')
        val = _clean_currency(value)
        if val is None:
            raise serializers.ValidationError('Invalid currency format.')
        return val

    def validate_existing_loans(self, value: str) -> str:
        _choice_validator(EXISTING_LOAN_CHOICES, 'loan type')(value)
        return value

    def validate_upi_usage(self, value: str) -> str:
        _choice_validator(UPI_USAGE_CHOICES, 'UPI usage frequency')(value)
        return value

    def validate_bill_payment_habit(self, value: str) -> str:
        _choice_validator(BILL_PAYMENT_CHOICES, 'bill payment habit')(value)
        return value


class Step3Serializer(serializers.Serializer):
    """Step 3 — Investment Profile."""

    investment_experience = serializers.CharField(max_length=50)
    emergency_fund = serializers.CharField(max_length=50)
    monthly_investment_budget = serializers.CharField(max_length=50)
    financial_goal = serializers.CharField(max_length=50)
    risk_preference = serializers.CharField(max_length=50)
    investment_duration = serializers.CharField(max_length=50)

    def validate_investment_experience(self, value: str) -> str:
        _choice_validator(INVESTMENT_EXPERIENCE_CHOICES, 'investment experience')(value)
        return value

    def validate_emergency_fund(self, value: str) -> str:
        _choice_validator(EMERGENCY_FUND_CHOICES, 'emergency fund')(value)
        return value

    def validate_monthly_investment_budget(self, value: str) -> Decimal:
        value = value.strip()
        if not value:
            raise serializers.ValidationError('Monthly investment budget is required.')
        val = _clean_currency(value)
        if val is None:
            raise serializers.ValidationError('Invalid currency format.')
        return val

    def validate_financial_goal(self, value: str) -> str:
        _choice_validator(FINANCIAL_GOAL_CHOICES, 'financial goal')(value)
        return value

    def validate_risk_preference(self, value: str) -> str:
        _choice_validator(RISK_PREFERENCE_CHOICES, 'risk preference')(value)
        return value

    def validate_investment_duration(self, value: str) -> str:
        _choice_validator(INVESTMENT_DURATION_CHOICES, 'investment duration')(value)
        return value


class ReviewSerializer(serializers.Serializer):
    """Read-only serializer for the full onboarding review (Step 4)."""

    # Personal
    full_name = serializers.CharField(read_only=True)
    age = serializers.IntegerField(read_only=True)
    gender = serializers.CharField(read_only=True)
    occupation = serializers.CharField(read_only=True)
    city = serializers.CharField(read_only=True)
    preferred_language = serializers.CharField(read_only=True)

    # Financial
    monthly_income = serializers.SerializerMethodField()
    monthly_expenses = serializers.SerializerMethodField()
    savings = serializers.SerializerMethodField()
    existing_loans = serializers.CharField(read_only=True)
    upi_usage = serializers.CharField(read_only=True)
    bill_payment_habit = serializers.CharField(read_only=True)

    # Investment
    investment_experience = serializers.CharField(read_only=True)
    emergency_fund = serializers.CharField(read_only=True)
    monthly_investment_budget = serializers.SerializerMethodField()
    financial_goal = serializers.CharField(read_only=True)
    risk_preference = serializers.CharField(read_only=True)
    investment_duration = serializers.CharField(read_only=True)

    def get_monthly_income(self, obj) -> str:
        return _format_currency(obj.monthly_income)
        
    def get_monthly_expenses(self, obj) -> str:
        return _format_currency(obj.monthly_expenses)
        
    def get_savings(self, obj) -> str:
        return _format_currency(obj.savings)
        
    def get_monthly_investment_budget(self, obj) -> str:
        return _format_currency(obj.monthly_investment_budget, ' / month')

    # Progress
    current_step = serializers.IntegerField(read_only=True)
    step1_completed = serializers.BooleanField(read_only=True)
    step2_completed = serializers.BooleanField(read_only=True)
    step3_completed = serializers.BooleanField(read_only=True)
    onboarding_completed = serializers.BooleanField(read_only=True)
