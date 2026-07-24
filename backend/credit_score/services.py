"""
Service Layer for Credit Score Module.
Orchestrates calculation, explanation generation, and DB updates using single-responsibility generators.
"""
from django.utils import timezone
from onboarding.models import UserProfile
from .metrics import FinancialMetricsCalculator
from .scoring import WeightedScoringEngine
from .generators import HistoryGenerator, BreakdownGenerator, ExplanationGenerator, RecommendationGenerator
from .constants import FEATURE_LABELS, METRIC_WEIGHTS

class CreditScoreService:
    """Service to generate and persist credit scores."""

    @staticmethod
    def get_or_calculate_credit_profile(user) -> dict:
        """
        Retrieves user profile, runs the scoring pipeline, saves the score,
        and returns the full structured dictionary for the API.
        """
        profile = getattr(user, 'profile', None)
        if not profile:
            raise ValueError("User profile not found. Complete onboarding first.")
            
        if not profile.monthly_income:
            raise ValueError("Incomplete financial data. Update profile to generate score.")

        # 1. Financial Metrics Calculator
        metrics_data = FinancialMetricsCalculator(profile).calculate()

        # 2. Weighted Scoring Engine
        score_data = WeightedScoringEngine(metrics_data).calculate()

        # 3. Save to DB
        profile.credit_score = score_data["credit_score"]
        profile.risk_score = score_data["risk_score"]
        profile.save(update_fields=['credit_score', 'risk_score', 'updated_at'])

        # 4. History Generator
        history = HistoryGenerator(score_data["credit_score"]).generate()

        # 5. Explanations Generator
        explanations = ExplanationGenerator(metrics_data, profile).generate()

        # 6. Recommendations Generator
        recommendations = RecommendationGenerator(metrics_data, profile).generate()

        # 7. Breakdown Generator
        breakdown = BreakdownGenerator(metrics_data["scores"]).generate()

        # 8. Feature Importance (Dynamic based on weights and actual score impact)
        feature_importance = []
        prog_colors = ["green", "blue", "indigo", "cyan", "purple", "orange"]
        idx = 0
        
        # Calculate maximum possible impact sum vs actual
        for key, raw_score in metrics_data["scores"].items():
            weight = METRIC_WEIGHTS.get(key, 0)
            actual_contribution = (raw_score * weight) 
            # Normalize to 0-100 based on weight
            normalized_pct = int((actual_contribution / (100 * weight)) * 100) if weight > 0 else 0
            
            label = FEATURE_LABELS.get(key, key)
            feature_importance.append({
                "label": label,
                "percentage": normalized_pct,
                "color_class": prog_colors[idx % len(prog_colors)]
            })
            idx += 1
            
        feature_importance = sorted(feature_importance, key=lambda x: x["percentage"], reverse=True)

        # Assemble Final API Payload exactly as requested
        return {
            "score": score_data["credit_score"],
            "grade": score_data["grade"],
            "risk_level": score_data["risk_level"],
            "category": score_data["category"],
            "risk_score": score_data["risk_score"],
            "financial_metrics": metrics_data["raw"],
            "feature_importance": feature_importance,
            "positive_factors": explanations["positive_factors"],
            "negative_factors": explanations["negative_factors"],
            "breakdown": breakdown,
            "history": history,
            "recommendations": recommendations,
            "ai_explanations": explanations["ai_explanations"],
            "updated_at": profile.updated_at.strftime("%B %d, %Y")
        }
