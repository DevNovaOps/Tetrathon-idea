"""Business logic for onboarding steps — keeps views thin."""
import logging

from django.db import transaction

from accounts.models import User
from .models import UserProfile

logger = logging.getLogger('onboarding')


def _get_or_create_profile(user: User) -> UserProfile:
    """Get existing profile or create one."""
    profile, created = UserProfile.objects.get_or_create(user=user)
    if created:
        logger.debug('Profile auto-created for %s', user.email)
    return profile


@transaction.atomic
def save_step1(user: User, data: dict) -> UserProfile:
    """Persist Step 1 — Personal Information."""
    profile = _get_or_create_profile(user)

    profile.full_name = data['full_name']
    profile.age = data['age']
    profile.gender = data['gender']
    profile.occupation = data['occupation']
    profile.city = data['city']
    profile.preferred_language = data['preferred_language']

    profile.step1_completed = True
    if profile.current_step < 2:
        profile.current_step = 2

    profile.save()
    logger.info('Step 1 saved for user: %s', user.email)
    return profile


@transaction.atomic
def save_step2(user: User, data: dict) -> UserProfile:
    """Persist Step 2 — Financial Profile."""
    profile = _get_or_create_profile(user)

    profile.monthly_income = data['monthly_income']
    profile.monthly_expenses = data['monthly_expenses']
    profile.savings = data['savings']
    profile.existing_loans = data['existing_loans']
    profile.upi_usage = data['upi_usage']
    profile.bill_payment_habit = data['bill_payment_habit']

    profile.step2_completed = True
    if profile.current_step < 3:
        profile.current_step = 3

    profile.save()
    logger.info('Step 2 saved for user: %s', user.email)
    return profile


@transaction.atomic
def save_step3(user: User, data: dict) -> UserProfile:
    """Persist Step 3 — Investment Profile."""
    profile = _get_or_create_profile(user)

    profile.investment_experience = data['investment_experience']
    profile.emergency_fund = data['emergency_fund']
    profile.monthly_investment_budget = data['monthly_investment_budget']
    profile.financial_goal = data['financial_goal']
    profile.risk_preference = data['risk_preference']
    profile.investment_duration = data['investment_duration']

    profile.step3_completed = True
    if profile.current_step < 4:
        profile.current_step = 4

    profile.save()
    logger.info('Step 3 saved for user: %s', user.email)
    return profile


@transaction.atomic
def finish_onboarding(user: User) -> UserProfile:
    """
    Mark onboarding as complete.
    Requires all three steps to be done.
    """
    profile = _get_or_create_profile(user)

    if not all([profile.step1_completed, profile.step2_completed, profile.step3_completed]):
        raise ValueError('All onboarding steps must be completed before finishing.')

    profile.onboarding_completed = True
    profile.save(update_fields=['onboarding_completed', 'updated_at'])

    # Also update the User model flag
    user.onboarding_completed = True
    user.save(update_fields=['onboarding_completed', 'updated_at'])

    logger.info('Onboarding completed for user: %s', user.email)
    return profile
