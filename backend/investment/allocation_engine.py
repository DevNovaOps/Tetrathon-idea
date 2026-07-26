class AllocationEngine:
    """
    Deterministically generates portfolio allocation totaling exactly 100%.
    """
    
    @staticmethod
    def generate_allocation(risk_bucket: str) -> list:
        # Default fallback
        allocation = [
            {"name": "Index Funds", "pct": 40, "cagr": "10-12%", "risk": "Moderate", "rec": True},
            {"name": "Debt Funds", "pct": 30, "cagr": "6-8%", "risk": "Low", "rec": False},
            {"name": "Gold ETFs", "pct": 10, "cagr": "8-10%", "risk": "Low", "rec": False},
            {"name": "Liquid Funds", "pct": 10, "cagr": "4-6%", "risk": "Very Low", "rec": False},
            {"name": "Blue Chip Stocks", "pct": 10, "cagr": "12-15%", "risk": "Moderate", "rec": False},
        ]
        
        if risk_bucket == "Low":
            allocation = [
                {"name": "Debt Funds", "pct": 45, "cagr": "6-8%", "risk": "Low", "rec": True},
                {"name": "Liquid Funds", "pct": 20, "cagr": "4-6%", "risk": "Very Low", "rec": False},
                {"name": "Gold ETFs", "pct": 20, "cagr": "8-10%", "risk": "Low", "rec": False},
                {"name": "Index Funds", "pct": 10, "cagr": "10-12%", "risk": "Moderate", "rec": False},
                {"name": "Blue Chip Stocks", "pct": 5, "cagr": "12-15%", "risk": "Moderate", "rec": False},
            ]
        elif risk_bucket == "Moderate":
            allocation = [
                {"name": "Index Funds", "pct": 40, "cagr": "10-12%", "risk": "Moderate", "rec": True},
                {"name": "Debt Funds", "pct": 20, "cagr": "6-8%", "risk": "Low", "rec": False},
                {"name": "Gold ETFs", "pct": 20, "cagr": "8-10%", "risk": "Low", "rec": False},
                {"name": "Liquid Funds", "pct": 10, "cagr": "4-6%", "risk": "Very Low", "rec": False},
                {"name": "Blue Chip Stocks", "pct": 10, "cagr": "12-15%", "risk": "Moderate", "rec": False},
            ]
        elif risk_bucket == "High":
            allocation = [
                {"name": "Index Funds", "pct": 55, "cagr": "10-12%", "risk": "Moderate", "rec": True},
                {"name": "Blue Chip Stocks", "pct": 20, "cagr": "12-15%", "risk": "Moderate", "rec": True},
                {"name": "Gold ETFs", "pct": 10, "cagr": "8-10%", "risk": "Low", "rec": False},
                {"name": "Debt Funds", "pct": 10, "cagr": "6-8%", "risk": "Low", "rec": False},
                {"name": "Liquid Funds", "pct": 5, "cagr": "4-6%", "risk": "Very Low", "rec": False},
            ]
            
        return allocation
        
    @staticmethod
    def calculate_weighted_cagr(allocation: list) -> float:
        """Calculates expected portfolio CAGR based on weights."""
        total_cagr = 0.0
        for asset in allocation:
            # Parse average from range e.g. "10-12%" -> 11
            cagr_range = asset["cagr"].replace('%', '').split('-')
            if len(cagr_range) == 2:
                avg_cagr = (float(cagr_range[0]) + float(cagr_range[1])) / 2
            else:
                avg_cagr = float(cagr_range[0])
            
            weight = asset["pct"] / 100.0
            total_cagr += avg_cagr * weight
            
        return round(total_cagr, 1)

    @staticmethod
    def generate_multi_scenario_allocation(risk_bucket: str, snapshot: dict) -> list:
        """
        Generates 3 different portfolio allocations based on the base risk_bucket.
        Provides reasoning for why each might be suitable.
        """
        scenarios = []
        
        if risk_bucket == "Low":
            scenarios = [
                {"scenario_name": "Conservative (Recommended)", "allocation": AllocationEngine.generate_allocation("Low"), "reason": "Prioritizes capital protection, aligning perfectly with your low risk tolerance."},
                {"scenario_name": "Balanced", "allocation": AllocationEngine.generate_allocation("Moderate"), "reason": "Slightly more equity exposure for better inflation-beating returns, suitable if you can extend your investment horizon."},
                {"scenario_name": "Ultra Safe", "allocation": [
                    {"name": "Debt Funds", "pct": 60, "cagr": "6-8%", "risk": "Low", "rec": True},
                    {"name": "Liquid Funds", "pct": 30, "cagr": "4-6%", "risk": "Very Low", "rec": False},
                    {"name": "Gold ETFs", "pct": 10, "cagr": "8-10%", "risk": "Low", "rec": False},
                ], "reason": "Zero equity exposure. Ideal for short-term goals where capital preservation is the absolute priority."}
            ]
        elif risk_bucket == "High":
            scenarios = [
                {"scenario_name": "Aggressive (Recommended)", "allocation": AllocationEngine.generate_allocation("High"), "reason": "Maximizes wealth creation over the long term, taking full advantage of your high risk tolerance."},
                {"scenario_name": "Balanced", "allocation": AllocationEngine.generate_allocation("Moderate"), "reason": "Reduces volatility during market downturns while still providing solid growth."},
                {"scenario_name": "Ultra Aggressive", "allocation": [
                    {"name": "Small/Mid Cap Stocks", "pct": 40, "cagr": "15-18%", "risk": "High", "rec": True},
                    {"name": "Index Funds", "pct": 40, "cagr": "10-12%", "risk": "Moderate", "rec": False},
                    {"name": "Blue Chip Stocks", "pct": 20, "cagr": "12-15%", "risk": "Moderate", "rec": False},
                ], "reason": "100% equity for maximum possible growth, suitable only for 10+ year horizons."}
            ]
        else: # Moderate
            scenarios = [
                {"scenario_name": "Balanced (Recommended)", "allocation": AllocationEngine.generate_allocation("Moderate"), "reason": "A perfect balance of growth and stability, matching your moderate risk profile."},
                {"scenario_name": "Conservative", "allocation": AllocationEngine.generate_allocation("Low"), "reason": "Focuses more on stability, suitable if you expect to need this money in the near future."},
                {"scenario_name": "Aggressive", "allocation": AllocationEngine.generate_allocation("High"), "reason": "Increases equity exposure for higher potential returns, suitable if your income is very stable."}
            ]
            
        return scenarios
