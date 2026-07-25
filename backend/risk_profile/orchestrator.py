from django.db import transaction
from .models import RiskProfile, RiskFeature, RiskRecommendation
from .financial_snapshot_service import FinancialSnapshotService
from .risk_engine import RiskEngine
from .explainability_engine import ExplainabilityEngine
from .recommendation_engine import RecommendationEngine
from .history_service import HistoryService
from .feature_importance import FeatureImportanceEngine
from .investment_mapper import InvestmentMapper

class RiskProfileOrchestrator:
    """
    Executes the entire Risk Profile workflow:
    Snapshot -> Risk -> Explainability -> Recommendation -> DB Save -> History
    """
    
    @staticmethod
    @transaction.atomic
    def run_pipeline(user):
        # 1. Financial Snapshot
        try:
            snapshot = FinancialSnapshotService.generate_snapshot(user)
        except ValueError:
            return None # User has no profile yet
            
        # 2. Risk Engine
        risk_results = RiskEngine.calculate(snapshot)
        
        # 3. Feature Importance
        features = FeatureImportanceEngine.calculate(snapshot, risk_results)
        
        # 4. Explainability Engine
        explanations = ExplainabilityEngine.generate_explanations(risk_results, features)
        
        # 5. Recommendation Engine
        recommendations = RecommendationEngine.generate_recommendations(risk_results)
        
        # 6. Investment Mapping
        portfolio = InvestmentMapper.generate_portfolio(snapshot, risk_results)
        
        # 7. DB Save (RiskProfile)
        profile_obj, _ = RiskProfile.objects.update_or_create(
            user=user,
            defaults={
                "monthly_income": snapshot["monthly_income"],
                "monthly_expenses": snapshot["monthly_expenses"],
                "monthly_savings": snapshot["monthly_savings"],
                "savings_rate_pct": risk_results["savings_rate"],
                "expense_ratio_pct": risk_results["expense_ratio"],
                "monthly_surplus": risk_results["monthly_surplus"],
                "emergency_coverage_months": risk_results["emergency_coverage"],
                "risk_score": risk_results["risk_score"],
                "risk_bucket": risk_results["risk_bucket"],
                "confidence_score": risk_results["confidence_score"],
                "investment_readiness": risk_results["investment_readiness"],
                "investment_readiness_pct": risk_results["investment_readiness_pct"],
                "investment_readiness_reason": risk_results["investment_readiness_reason"],
                "ai_risk_explanation": explanations["ai_explanation"],
                "portfolio_allocation": portfolio,
            }
        )
        
        # Clear old features and insert new
        RiskFeature.objects.filter(risk_profile=profile_obj).delete()
        features_to_create = []
        for f in explanations["positive_factors"]:
            features_to_create.append(RiskFeature(
                risk_profile=profile_obj, feature_name=f["feature"],
                impact=f["impact"], reason=f["reason"], is_positive=True
            ))
        for f in explanations["negative_factors"]:
            features_to_create.append(RiskFeature(
                risk_profile=profile_obj, feature_name=f["feature"],
                impact=f["impact"], reason=f["reason"], is_positive=False
            ))
        RiskFeature.objects.bulk_create(features_to_create)
        
        # Clear old recommendations and insert new
        RiskRecommendation.objects.filter(risk_profile=profile_obj).delete()
        recs_to_create = []
        for r in recommendations:
            recs_to_create.append(RiskRecommendation(
                risk_profile=profile_obj, action=r["action"],
                reason=r["reason"], benefit=r["benefit"],
                risk_reduction_estimate=r["risk_reduction_estimate"], 
                estimated_credit_improvement=r["estimated_credit_improvement"],
                estimated_completion_time=r["estimated_completion_time"],
                priority=r["priority"]
            ))
        RiskRecommendation.objects.bulk_create(recs_to_create)
        
        # 6. Risk History Updated
        HistoryService.log_history_if_changed(
            user=user, 
            current_score=risk_results["risk_score"], 
            current_bucket=risk_results["risk_bucket"]
        )
        
        return profile_obj
