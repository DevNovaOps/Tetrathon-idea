"""
Service Layer for Credit Score Module.
Orchestrates calculation, explanation generation, and DB updates.
"""
from django.utils import timezone
from onboarding.models import UserProfile
from .metrics import FinancialMetricsCalculator
from .scoring import WeightedScoringEngine
from .explanations import ExplanationGenerator
from .constants import FEATURE_LABELS

class CreditScoreService:
    """Service to generate and persist credit scores."""

    @staticmethod
    def get_or_calculate_credit_profile(user) -> dict:
        """
        Retrieves user profile, runs the scoring engine, saves the score,
        and returns the full dictionary response for the API.
        """
        profile = getattr(user, 'profile', None)
        if not profile:
            raise ValueError("User profile not found. Complete onboarding first.")

        # 1. Calculate base sub-metrics (0-100)
        metrics_calc = FinancialMetricsCalculator(profile)
        sub_metrics = metrics_calc.calculate_all()

        # 2. Run Weighted Scoring Engine
        scoring_engine = WeightedScoringEngine(sub_metrics)
        score_data = scoring_engine.calculate()

        # 3. Save the results back to UserProfile
        profile.credit_score = score_data["credit_score"]
        profile.risk_score = score_data["risk_score"]
        profile.save(update_fields=['credit_score', 'risk_score', 'updated_at'])

        # 4. Generate Explanations
        explainer = ExplanationGenerator(profile, sub_metrics)
        explanations = explainer.generate_all()

        # 5. Format Breakdown and Feature Importance for UI
        breakdown = []
        feature_importance = []
        
        # Color mapping for UI elements
        color_map = {
            "payment_behaviour": {"bg": "green-bg", "text": "green-text", "hex": "#10B981", "icon": "💳"},
            "savings_habit": {"bg": "blue-bg", "text": "blue-text", "hex": "#3B82F6", "icon": "🏦"},
            "financial_stability": {"bg": "purple-bg", "text": "purple-text", "hex": "#A855F7", "icon": "📊"},
            "investment_behaviour": {"bg": "cyan-bg", "text": "cyan-text", "hex": "#06B6D4", "icon": "📈"},
            "upi_activity": {"bg": "indigo-bg", "text": "indigo-text", "hex": "#6366F1", "icon": "📱"},
            "utility_bills": {"bg": "emerald-bg", "text": "emerald-text", "hex": "#059669", "icon": "⚡"},
        }
        
        prog_colors = ["green", "blue", "indigo", "cyan", "purple", "orange"]
        idx = 0

        for key, val in sub_metrics.items():
            label = FEATURE_LABELS.get(key, key)
            c = color_map.get(key, color_map["payment_behaviour"])
            
            # Breakdown Card
            breakdown.append({
                "key": key,
                "title": label,
                "percentage": val,
                "icon": c["icon"],
                "bg_class": c["bg"],
                "text_class": c["text"],
                "hex_color": c["hex"]
            })
            
            # Feature Importance Bar
            feature_importance.append({
                "label": label,
                "percentage": val,
                "color_class": prog_colors[idx % len(prog_colors)]
            })
            idx += 1
            
        # Sort feature importance by highest impact (highest score)
        feature_importance = sorted(feature_importance, key=lambda x: x["percentage"], reverse=True)

        return {
            "score": score_data["credit_score"],
            "grade": score_data["grade"],
            "risk_level": score_data["risk_level"],
            "category": score_data["category"],
            "risk_score": score_data["risk_score"],
            "positive_factors": explanations["positive_factors"],
            "negative_factors": explanations["negative_factors"],
            "feature_importance": feature_importance,
            "breakdown": breakdown,
            "history": score_data["history"],
            "recommendations": explanations["recommendations"],
            "ai_explanations": explanations["ai_explanations"],
            "updated_at": profile.updated_at.strftime("%B %d, %Y")
        }
