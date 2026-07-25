class GoalForecastEngine:
    """
    Compares simulation against user's target.
    """
    @staticmethod
    def forecast_progress(future_value: int, target_value: int, years: int) -> dict:
        progress_pct = 0
        if target_value > 0:
            progress_pct = min(100, int((future_value / target_value) * 100))
            
        status = "On Track"
        if progress_pct < 80:
            status = "Needs Attention"
        elif progress_pct < 50:
            status = "Delayed"
            
        return {
            "name": "Primary Investment Goal",
            "target": target_value,
            "current": future_value,
            "progress_pct": progress_pct,
            "status": status,
            "estimated_completion": f"{years} Years"
        }
