from django.db.models.signals import post_save
from django.dispatch import receiver
from onboarding.models import UserProfile
from ai_assistant.models import Conversation, AssessmentAnswer
from .orchestrator import RiskProfileOrchestrator

@receiver(post_save, sender=UserProfile)
def trigger_risk_profile_on_user_update(sender, instance, created, **kwargs):
    """
    Recalculate risk profile when core financial data or credit score changes on the UserProfile.
    """
    # Exclude raw creates where fields might not be populated yet to avoid spamming
    if not created:
        RiskProfileOrchestrator.run_pipeline(instance.user)


@receiver(post_save, sender=Conversation)
def trigger_risk_profile_on_ai_conversation(sender, instance, **kwargs):
    """
    Recalculate risk profile when an AI conversation is completed.
    """
    if instance.completed:
        RiskProfileOrchestrator.run_pipeline(instance.user)


@receiver(post_save, sender=AssessmentAnswer)
def trigger_risk_profile_on_ai_answer(sender, instance, **kwargs):
    """
    Recalculate if individual answers change the snapshot.
    """
    # For safety, updating individual answers also triggers it.
    RiskProfileOrchestrator.run_pipeline(instance.conversation.user)
