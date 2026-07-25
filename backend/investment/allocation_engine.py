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
