from risk_profile.financial_snapshot_service import FinancialSnapshotService
from risk_profile.risk_engine import RiskEngine
from .models import InvestmentProfile, PortfolioAsset, InvestmentGuidance, PortfolioBenefit
from .allocation_engine import AllocationEngine
from .projection_engine import ProjectionEngine
from .goal_engine import GoalEngine
from .ai_guidance_engine import AIGuidanceEngine

class InvestmentOrchestrator:
    """
    Coordinates the AI Investment Recommendation pipeline.
    Consumes Risk Profile and Dashboard data to generate investment plans.
    """
    
    @staticmethod
    def run_pipeline(user):
        # 1. Financial Snapshot & Risk Results (Consume, do not recalculate independently if possible)
        snapshot = FinancialSnapshotService.generate_snapshot(user)
        risk_results = RiskEngine.calculate(snapshot)
        
        # 2. Investment Goal / SIP Engine
        goal_data = GoalEngine.generate_primary_goal(snapshot, risk_results)
        monthly_sip = goal_data["monthly_sip"]
        horizon_years = goal_data["horizon_years"]
        
        # 3. Allocation Engine
        allocation = AllocationEngine.generate_allocation(risk_results["risk_bucket"])
        expected_cagr = AllocationEngine.calculate_weighted_cagr(allocation)
        
        # 4. Projection Engine
        target_value = ProjectionEngine.calculate_future_value(monthly_sip, horizon_years, expected_cagr)
        
        # 5. AI Guidance & Benefits
        guidance = AIGuidanceEngine.generate_guidance(snapshot, risk_results, allocation)
        benefits = AIGuidanceEngine.generate_benefits(allocation)
        
        # 6. Database Save
        profile_obj, _ = InvestmentProfile.objects.update_or_create(
            user=user,
            defaults={
                "monthly_sip": monthly_sip,
                "target_value": target_value,
                "horizon_years": horizon_years,
                "expected_cagr": f"{expected_cagr}%",
                "confidence_score": risk_results["confidence_score"],
                "risk_bucket": risk_results["risk_bucket"]
            }
        )
        
        # Save Allocation
        PortfolioAsset.objects.filter(profile=profile_obj).delete()
        assets_to_create = []
        for a in allocation:
            assets_to_create.append(PortfolioAsset(
                profile=profile_obj,
                name=a["name"],
                allocation_pct=a["pct"],
                expected_cagr_range=a["cagr"],
                risk_level=a["risk"],
                is_highly_recommended=a["rec"]
            ))
        PortfolioAsset.objects.bulk_create(assets_to_create)
        
        # Save Guidance
        InvestmentGuidance.objects.filter(profile=profile_obj).delete()
        guidance_to_create = [
            InvestmentGuidance(profile=profile_obj, action=g["action"], reason=g["reason"], color_theme=g["color"])
            for g in guidance
        ]
        InvestmentGuidance.objects.bulk_create(guidance_to_create)
        
        # Save Benefits
        PortfolioBenefit.objects.filter(profile=profile_obj).delete()
        benefits_to_create = [
            PortfolioBenefit(profile=profile_obj, title=b["title"], description=b["desc"], color_theme=b["color"], emoji=b["emoji"])
            for b in benefits
        ]
        PortfolioBenefit.objects.bulk_create(benefits_to_create)
        
        return profile_obj
