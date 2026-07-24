"""Custom User model — email-based, OAuth-ready."""
import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .constants import AUTH_PROVIDER_CHOICES, AUTH_PROVIDER_EMAIL, COUNTRY_CHOICES
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user with email as the unique identifier.
    Stores auth-provider metadata (Google) and onboarding status.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True, db_index=True)
    phone = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=10, choices=COUNTRY_CHOICES, blank=True)

    # OAuth fields
    auth_provider = models.CharField(
        max_length=20,
        choices=AUTH_PROVIDER_CHOICES,
        default=AUTH_PROVIDER_EMAIL,
    )
    google_id = models.CharField(max_length=255, blank=True)
    profile_picture = models.URLField(max_length=500, blank=True)

    # Status flags
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    onboarding_completed = models.BooleanField(default=False)

    # Production tracking and localization
    last_activity = models.DateTimeField(null=True, blank=True)
    login_count = models.PositiveIntegerField(default=0)
    timezone = models.CharField(max_length=50, default='UTC')
    preferred_currency = models.CharField(max_length=10, default='INR')

    # Timestamps
    date_joined = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # email is already required by USERNAME_FIELD

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']

    def __str__(self) -> str:
        return self.email

    @property
    def display_name(self) -> str:
        return self.full_name or self.email.split('@')[0]
