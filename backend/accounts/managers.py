"""Custom user manager — email-based authentication."""
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """Manager for the custom User model (email as login identifier)."""

    def create_user(self, email: str, password: str | None = None, **extra_fields):
        """Create and return a regular user with a hashed password."""
        if not email:
            raise ValueError('Email address is required.')

        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str | None = None, **extra_fields):
        """Create and return a superuser."""
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        extra_fields['is_verified'] = True

        if password is None:
            raise ValueError('Superuser must have a password.')

        return self.create_user(email, password, **extra_fields)
