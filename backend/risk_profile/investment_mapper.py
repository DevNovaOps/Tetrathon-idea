class InvestmentMapper:
    """
    Dynamically generates a personalized portfolio allocation.
    """
    
    @staticmethod
    def generate_portfolio(snapshot: dict, risk_results: dict) -> list:
        score = risk_results["risk_score"]
        preference = str(snapshot.get("risk_preference", "")).lower()
        experience = str(snapshot.get("investment_experience", "")).lower()
        
        portfolio = []
        
        # Safe / Low Risk
        if score < 50 or "low" in preference or "beginner" in experience:
            portfolio = [
                {"name": "Index Funds", "allocation_pct": 30, "cagr": "10-12%", "risk": "Moderate"},
                {"name": "Debt Funds", "allocation_pct": 40, "cagr": "6-8%", "risk": "Low"},
                {"name": "Gold ETFs", "allocation_pct": 10, "cagr": "8-10%", "risk": "Low"},
                {"name": "Liquid Funds", "allocation_pct": 20, "cagr": "4-6%", "risk": "Very Low"},
            ]
        # Moderate Risk
        elif score < 75 or "medium" in preference or "moderate" in preference:
            portfolio = [
                {"name": "Index Funds", "allocation_pct": 50, "cagr": "10-12%", "risk": "Moderate"},
                {"name": "Flexi Cap Funds", "allocation_pct": 20, "cagr": "12-14%", "risk": "High"},
                {"name": "Debt Funds", "allocation_pct": 20, "cagr": "6-8%", "risk": "Low"},
                {"name": "Gold ETFs", "allocation_pct": 10, "cagr": "8-10%", "risk": "Low"},
            ]
        # High Risk / Aggressive
        else:
            portfolio = [
                {"name": "Small/Mid Cap Funds", "allocation_pct": 40, "cagr": "15-18%", "risk": "Very High"},
                {"name": "Index Funds", "allocation_pct": 40, "cagr": "10-12%", "risk": "Moderate"},
                {"name": "Direct Equity", "allocation_pct": 15, "cagr": "15-20%", "risk": "Very High"},
                {"name": "Liquid Funds", "allocation_pct": 5, "cagr": "4-6%", "risk": "Very Low"},
            ]
            
        return portfolio
