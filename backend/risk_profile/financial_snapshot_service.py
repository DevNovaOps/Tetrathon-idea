from onboarding.models import UserProfile
from ai_assistant.models import Conversation

class FinancialSnapshotService:
    """
    Centralized Financial Snapshot Engine.
    Becomes the Single Source of Truth by aggregating data across modules.
    """
    
    @staticmethod
    def generate_snapshot(user) -> dict:
        """
        Gathers raw data from UserProfile, CreditScore, ImproveScore, and AIAssistant.
        Returns a structured dictionary of metrics for the Risk Engine.
        """
        profile = getattr(user, 'profile', None)
        if not profile:
            raise ValueError("User profile not found. Complete onboarding first.")

        # Extract base financials from Profile
        monthly_income = float(profile.monthly_income) if profile.monthly_income else 0.0
        monthly_expenses = float(profile.monthly_expenses) if profile.monthly_expenses else 0.0
        monthly_savings = float(profile.savings) if profile.savings else 0.0
        credit_score = profile.credit_score or 0

        # Enhance with AI Assistant data if available
        # AI Assistant questions overwrite Profile data if they are more recent/detailed.
        ai_conversation = Conversation.objects.filter(user=user, completed=True).order_by('-updated_at').first()
        investment_experience = profile.investment_experience
        risk_preference = profile.risk_preference
        emergency_fund_status = profile.emergency_fund

        if ai_conversation:
            for answer in ai_conversation.answers.all():
                key = answer.question_key
                # Use parsed numeric value if available
                val = answer.numeric_value if answer.numeric_value is not None else answer.answer
                
                if key == 'monthly_income' and val:
                    monthly_income = float(val)
                elif key == 'monthly_expenses' and val:
                    monthly_expenses = float(val)
                elif key == 'current_savings' and val:
                    monthly_savings = float(val)
                elif key == 'emergency_fund' and val:
                    emergency_fund_status = str(val)
                elif key == 'investment_experience' and val:
                    investment_experience = str(val)
                elif key == 'risk_tolerance' and val:
                    risk_preference = str(val)

        return {
            "monthly_income": monthly_income,
            "monthly_expenses": monthly_expenses,
            "monthly_savings": monthly_savings,
            "credit_score": credit_score,
            "emergency_fund_status": emergency_fund_status,
            "investment_experience": investment_experience,
            "risk_preference": risk_preference,
        }
