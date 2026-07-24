"""Serializers for authentication endpoints."""
import re

from rest_framework import serializers

from .constants import PASSWORD_MIN_LENGTH, PASSWORD_RULES_MESSAGE, VALID_COUNTRY_CODES


class RegisterSerializer(serializers.Serializer):
    """Validates registration input."""

    full_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    country = serializers.CharField(max_length=10, required=False, allow_blank=True)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    # ── Field-level validations ─────────────────────────────────────────
    def validate_full_name(self, value: str) -> str:
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError('Full name must be at least 2 characters.')
        return value

    def validate_email(self, value: str) -> str:
        from .models import User
        value = value.lower().strip()
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('An account with this email already exists.')
        return value

    def validate_phone(self, value: str) -> str:
        if value:
            cleaned = re.sub(r'[\s\-()]', '', value)
            if not re.match(r'^\+?\d{7,15}$', cleaned):
                raise serializers.ValidationError(
                    'Enter a valid phone number (7-15 digits, optional + prefix).'
                )
        return value

    def validate_country(self, value: str) -> str:
        if value and value.upper() not in VALID_COUNTRY_CODES:
            raise serializers.ValidationError(
                f'Unsupported country code. Allowed: {", ".join(sorted(VALID_COUNTRY_CODES))}'
            )
        return value.upper() if value else ''

    def validate_password(self, value: str) -> str:
        if len(value) < PASSWORD_MIN_LENGTH:
            raise serializers.ValidationError(PASSWORD_RULES_MESSAGE)
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError(PASSWORD_RULES_MESSAGE)
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError(PASSWORD_RULES_MESSAGE)
        if not re.search(r'\d', value):
            raise serializers.ValidationError(PASSWORD_RULES_MESSAGE)
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError(PASSWORD_RULES_MESSAGE)
        return value

    # ── Cross-field validation ──────────────────────────────────────────
    def validate(self, attrs: dict) -> dict:
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'confirm_password': 'Passwords do not match.'})
        return attrs


class LoginSerializer(serializers.Serializer):
    """Validates login input."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    remember_me = serializers.BooleanField(required=False, default=False)

    def validate_email(self, value: str) -> str:
        return value.lower().strip()


class UserSerializer(serializers.Serializer):
    """Read-only serializer for the authenticated user."""

    id = serializers.UUIDField(read_only=True)
    full_name = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    phone = serializers.CharField(read_only=True)
    country = serializers.CharField(read_only=True)
    auth_provider = serializers.CharField(read_only=True)
    profile_picture = serializers.URLField(read_only=True)
    is_verified = serializers.BooleanField(read_only=True)
    onboarding_completed = serializers.BooleanField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
