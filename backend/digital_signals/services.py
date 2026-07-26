"""
Service layer for Digital Signals module.
Handles CRUD, feature derivation, and cascading credit score updates.
"""
from .models import DigitalSignalProfile
from .feature_engine import DigitalFeatureEngine


class DigitalSignalService:

    @staticmethod
    def get_or_create(user):
        """Returns existing signal profile or creates a default one."""
        profile, created = DigitalSignalProfile.objects.get_or_create(user=user)
        return profile

    @staticmethod
    def get_full_profile(user) -> dict:
        """Returns raw signals + derived features for the API."""
        profile = DigitalSignalService.get_or_create(user)
        engine = DigitalFeatureEngine(profile)
        features = engine.calculate_all()

        return {
            "signals": {
                "electricity_bill_frequency": profile.electricity_bill_frequency,
                "water_bill_frequency": profile.water_bill_frequency,
                "gas_bill_frequency": profile.gas_bill_frequency,
                "mobile_recharge_frequency": profile.mobile_recharge_frequency,
                "broadband_payment": profile.broadband_payment,
                "upi_transaction_frequency": profile.upi_transaction_frequency,
                "card_transaction_frequency": profile.card_transaction_frequency,
                "shopping_frequency": profile.shopping_frequency,
                "utility_payment_regularity": profile.utility_payment_regularity,
                "online_spending_behaviour": profile.online_spending_behaviour,
            },
            "derived_features": features,
            "updated_at": profile.updated_at.isoformat() if profile.updated_at else None,
        }

    @staticmethod
    def update_signals(user, data: dict):
        """
        Updates signal fields and triggers downstream cascades.
        Returns the updated profile dict.
        """
        profile = DigitalSignalService.get_or_create(user)

        updatable = [
            'electricity_bill_frequency', 'water_bill_frequency',
            'gas_bill_frequency', 'mobile_recharge_frequency',
            'broadband_payment', 'upi_transaction_frequency',
            'card_transaction_frequency', 'shopping_frequency',
            'utility_payment_regularity', 'online_spending_behaviour',
        ]

        changed = False
        for field in updatable:
            if field in data and data[field] is not None:
                setattr(profile, field, data[field])
                changed = True

        if changed:
            profile.save()  # post_save signal handles cascade

        return DigitalSignalService.get_full_profile(user)

    @staticmethod
    def get_credit_score_input(user) -> int:
        """Returns the single 0-100 score for the credit scoring engine."""
        try:
            profile = DigitalSignalProfile.objects.get(user=user)
            return DigitalFeatureEngine(profile).credit_score_contribution()
        except DigitalSignalProfile.DoesNotExist:
            return 50  # neutral default
