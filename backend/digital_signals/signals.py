"""
Cascade signals for Digital Signals module.
When signals change → recalculate credit score → recalculate risk profile.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DigitalSignalProfile


@receiver(post_save, sender=DigitalSignalProfile)
def cascade_on_digital_signal_change(sender, instance, created, **kwargs):
    """Recalculate credit score and risk profile when digital signals update."""
    if created:
        return  # Skip initial creation cascade

    user = instance.user

    # 1. Recalculate credit score (which now includes digital signals)
    try:
        from credit_score.services import CreditScoreService
        CreditScoreService.get_or_calculate_credit_profile(user)
    except Exception:
        pass

    # 2. Recalculate risk profile
    try:
        from risk_profile.orchestrator import RiskProfileOrchestrator
        RiskProfileOrchestrator.run_pipeline(user)
    except Exception:
        pass

    # 3. Record AI memory
    try:
        from ai_memory.memory_service import MemoryService
        from .feature_engine import DigitalFeatureEngine
        features = DigitalFeatureEngine(instance).calculate_all()
        MemoryService.record_memory(
            user=user,
            memory_type='behavior_change',
            title='Digital Signals Updated',
            summary=f"Digital financial activity score: {features['digital_financial_activity']}/100. "
                    f"Utility consistency: {features['utility_payment_consistency']}/100.",
            data=features
        )
    except Exception:
        pass
