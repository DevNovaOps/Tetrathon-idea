from investment.models import InvestmentProfile
from .compound_engine import CompoundEngine
from .scenario_engine import ScenarioEngine
from .chart_data_engine import ChartDataEngine
from .goal_forecast_engine import GoalForecastEngine
from .growth_insight_engine import GrowthInsightEngine
from .timeline_engine import TimelineEngine

class SimulationService:
    """
    Coordinates deterministic calculations without DB persistence.
    Supports goal-based simulation when goal_id is provided.
    """
    @staticmethod
    def run_simulation(user, sip_override=None, years_override=None, scenario_override=None, goal_id=None):
        profile = getattr(user, 'investment_profile', None)
        
        # Read defaults from profile or fallback
        base_sip = profile.monthly_sip if profile else 2000
        base_years = profile.horizon_years if profile else 5
        base_cagr_str = profile.expected_cagr if profile else "12.0%"
        target_value = profile.target_value if profile else 200000
        
        goal_info = None
        
        # If goal_id provided, use goal data instead of investment profile
        if goal_id:
            try:
                from user_profile.models import FinancialGoal
                goal = FinancialGoal.objects.get(id=goal_id, user=user, is_deleted=False)
                target_value = int(float(goal.target_amount))
                if goal.monthly_contribution and float(goal.monthly_contribution) > 0:
                    base_sip = int(float(goal.monthly_contribution))
                # Calculate years from deadline
                if goal.deadline:
                    from datetime import date
                    delta = (goal.deadline - date.today()).days
                    goal_years = max(1, delta // 365)
                    base_years = goal_years
                goal_info = {
                    "id": str(goal.id),
                    "name": goal.goal_name,
                    "type": goal.goal_type,
                    "target_amount": target_value,
                    "current_progress": float(goal.current_progress),
                    "monthly_contribution": base_sip,
                    "completion_percentage": float(goal.completion_percentage),
                    "status": goal.status,
                    "remaining": max(0, target_value - float(goal.current_progress)),
                }
            except Exception:
                pass
        
        try:
            base_cagr = float(base_cagr_str.replace('%', ''))
        except:
            base_cagr = 12.0
            
        # Apply overrides from request
        active_sip = int(sip_override) if sip_override else base_sip
        active_years = int(years_override) if years_override else base_years
        
        # Generate scenarios
        scenarios = ScenarioEngine.generate_scenarios(base_cagr)
        
        # Pick active scenario
        active_scenario_obj = next((s for s in scenarios if s["id"] == scenario_override), None)
        if not active_scenario_obj:
            active_scenario_obj = scenarios[1] # Default to moderate
            
        active_cagr = active_scenario_obj["cagr"]
        
        # Calculate metrics
        metrics = CompoundEngine.calculate_metrics(active_sip, active_years, active_cagr)
        
        # Inject scenario future values
        for scen in scenarios:
            scen["future_value"] = CompoundEngine.calculate_future_value(active_sip, active_years, scen["cagr"])
            
        # Generate chart data
        chart_data = ChartDataEngine.generate_datasets(active_sip, active_years, scenarios)
        
        # Goal progress
        goal_tracker = GoalForecastEngine.forecast_progress(metrics["future_value"], target_value, active_years)
        
        # Insights
        insights = GrowthInsightEngine.generate_insights(active_sip, active_years, active_cagr)
        
        # Timeline
        timeline = TimelineEngine.generate_timeline(active_sip, active_cagr, metrics["future_value"])
        
        # Available goals for selector
        available_goals = []
        try:
            from user_profile.models import FinancialGoal
            goals = FinancialGoal.objects.filter(user=user, is_deleted=False, status='Active')
            available_goals = [{
                "id": str(g.id),
                "name": g.goal_name,
                "type": g.goal_type,
                "target_amount": float(g.target_amount),
                "is_primary": g.is_primary,
            } for g in goals]
        except Exception:
            pass
        
        result = {
            "summary_metrics": {
                "monthly_sip": active_sip,
                "horizon_years": active_years,
                "expected_cagr": f"{active_cagr}%",
                "total_invested": metrics["total_invested"],
                "estimated_returns": metrics["estimated_returns"],
                "future_value": metrics["future_value"]
            },
            "active_scenario": active_scenario_obj["id"],
            "scenarios": scenarios,
            "chart_data": chart_data,
            "goal_tracker": goal_tracker,
            "ai_insights": insights,
            "timeline": timeline,
            "available_goals": available_goals,
            "educational_disclaimer": "This prototype provides educational financial insights only and does not constitute regulated financial advice."
        }
        
        if goal_info:
            result["goal_info"] = goal_info
        
        return result
