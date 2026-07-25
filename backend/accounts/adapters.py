"""Custom allauth adapters for Google OAuth integration."""
import logging

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialLogin
from django.urls import reverse

from .constants import AUTH_PROVIDER_GOOGLE

logger = logging.getLogger('accounts')


class CustomAccountAdapter(DefaultAccountAdapter):
    """Override default allauth account adapter."""

    def get_login_redirect_url(self, request):
        """Redirect after login based on onboarding status."""
        user = request.user
        if user.is_authenticated and user.onboarding_completed:
            return reverse('dashboard')
        return reverse('onboarding')

    def get_logout_redirect_url(self, request):
        """Redirect to landing page after logout."""
        return reverse('landing')


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """Handle Google OAuth login/signup."""

    def pre_social_login(self, request, sociallogin: SocialLogin):
        """
        If a user already exists with the same email, connect the
        Google account to the existing user instead of creating a new one.
        """
        if sociallogin.is_existing:
            return

        email = sociallogin.account.extra_data.get('email', '').lower()
        is_verified = sociallogin.account.extra_data.get('email_verified', False)
        if not email or not is_verified:
            # We don't link if the email isn't verified by Google
            return

        from .models import User

        try:
            existing_user = User.objects.get(email=email)
            sociallogin.connect(request, existing_user)
            logger.info('Google account linked to existing user: %s', email)
        except User.DoesNotExist:
            pass

    def save_user(self, request, sociallogin: SocialLogin, form=None):
        """Populate custom fields from Google data."""
        user = super().save_user(request, sociallogin, form)
        extra_data = sociallogin.account.extra_data

        user.auth_provider = AUTH_PROVIDER_GOOGLE
        user.google_id = sociallogin.account.uid or ''
        user.full_name = extra_data.get('name', '')
        user.profile_picture = extra_data.get('picture', '')
        user.is_verified = extra_data.get('email_verified', False)
        user.save(update_fields=[
            'auth_provider', 'google_id', 'full_name',
            'profile_picture', 'is_verified',
        ])

        logger.info('Google OAuth user created: %s', user.email)
        return user

    def populate_user(self, request, sociallogin, data):
        """Fill initial user fields from Google profile data."""
        user = super().populate_user(request, sociallogin, data)
        extra = sociallogin.account.extra_data
        user.full_name = extra.get('name', '')
        user.email = extra.get('email', '')
        return user
