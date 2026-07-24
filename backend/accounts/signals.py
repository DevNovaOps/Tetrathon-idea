"""Signals for the accounts app."""
import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger('accounts')


@receiver(post_save, sender='accounts.User')
def create_user_profile(sender, instance, created, **kwargs):
    """Auto-create a UserProfile whenever a new User is created."""
    if created:
        from onboarding.models import UserProfile
        UserProfile.objects.get_or_create(user=instance)
        logger.debug('UserProfile created for: %s', instance.email)
