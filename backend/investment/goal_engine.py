class GoalEngine:
    """
    Lightweight engine to dynamically generate a primary investment goal
    based on the user's financial capacity.
    """
    
    @staticmethod
    def generate_primary_goal(snapshot: dict, risk_results: dict):
        # Default horizon
        horizon_years = 5
        
        # Calculate surplus from snapshot
        income = float(snapshot.get("monthly_income", 0))
        expenses = float(snapshot.get("monthly_expenses", 0))
        surplus = max(0, income - expenses)
        
        # Recommended SIP is 20% of income, or 50% of surplus, whichever is lower
        # Minimum SIP 500
        target_sip = int(min(income * 0.2, surplus * 0.5))
        if target_sip < 500:
            target_sip = 500 if surplus >= 500 else 0
            
        return {
            "horizon_years": horizon_years,
            "monthly_sip": target_sip
        }
