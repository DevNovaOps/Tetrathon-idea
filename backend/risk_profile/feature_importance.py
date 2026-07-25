class FeatureImportanceEngine:
    """
    Calculates exact deterministic point contributions for each financial factor.
    """
    
    @staticmethod
    def calculate(snapshot: dict, risk_results: dict) -> list:
        subs = risk_results["sub_scores"]
        
        # Max theoretical points for each bucket
        # Savings Health: 25
        # Financial Stability (Income/Expenses): 25
        # Behavioral (Credit/Debt): 25
        # Emergency Fund: 25
        
        # Savings Rate Impact
        savings_health = subs["savings_health"]
        savings_points = int((savings_health / 100) * 25)
        # Shift to -12 to +13 range roughly? No, user wants +18, -15 type numbers.
        # Let's say baseline is 0. If health is 100, they get +15. If health is 0, they get -15.
        
        def scale_to_impact(score, max_points):
            # 50 is neutral (0 points). 100 is +max_points. 0 is -max_points.
            return int(((score - 50) / 50) * max_points)
            
        savings_impact = scale_to_impact(savings_health, 20)
        expense_impact = scale_to_impact(subs["financial_stability"], 20)
        credit_impact = scale_to_impact(subs["behavioral_risk"], 20)
        ef_impact = scale_to_impact(subs["emergency_fund_strength"], 20)
        
        # Additional factors
        investment_exp = snapshot.get("investment_experience", "").lower()
        if "advanced" in investment_exp or "expert" in investment_exp:
            inv_impact = 10
        elif "intermediate" in investment_exp:
            inv_impact = 5
        else:
            inv_impact = -6
            
        income = float(snapshot.get("monthly_income", 0))
        if income > 150000:
            income_impact = 12
        elif income > 80000:
            income_impact = 8
        elif income > 40000:
            income_impact = 3
        else:
            income_impact = -5
            
        # Compile list
        features = [
            {"feature": "Savings Rate", "impact": savings_impact},
            {"feature": "Emergency Fund", "impact": ef_impact},
            {"feature": "Income Stability", "impact": income_impact},
            {"feature": "Expense Ratio", "impact": expense_impact},
            {"feature": "Credit Health", "impact": credit_impact},
            {"feature": "Investment Experience", "impact": inv_impact},
        ]
        
        # Sort by impact magnitude (absolute value) descending, but let's just sort highest positive to lowest negative
        features = sorted(features, key=lambda x: x["impact"], reverse=True)
        return features
