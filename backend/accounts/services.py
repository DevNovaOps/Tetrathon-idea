"""Business logic for authentication — keeps views thin."""
import logging

from django.contrib.auth import authenticate
from django.db import transaction

from .constants import AUTH_PROVIDER_EMAIL
from .models import User

logger = logging.getLogger('accounts')


@transaction.atomic
def register_user(validated_data: dict) -> User:
    """Create a new user from validated registration data."""
    user = User.objects.create_user(
        email=validated_data['email'],
        password=validated_data['password'],
        full_name=validated_data['full_name'],
        phone=validated_data.get('phone', ''),
        country=validated_data.get('country', ''),
        auth_provider=AUTH_PROVIDER_EMAIL,
    )
    logger.info('New user registered: %s', user.email)
    return user


def authenticate_user(email: str, password: str) -> User | None:
    """Authenticate a user by email and password."""
    user = authenticate(email=email, password=password)
    if user is not None:
        logger.info('User authenticated: %s', email)
    else:
        logger.warning('Failed login attempt for: %s', email)
    return user
