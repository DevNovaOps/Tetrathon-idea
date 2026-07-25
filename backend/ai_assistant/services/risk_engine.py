class RiskEngine:
    """
    Deterministic rule engine that calculates risk_score (0-100) 
    and risk_level (Low, Moderate, High) strictly using the AssessmentAnswer data.
    """
    def __init__(self, answers: list):
        # answers is a list of dicts: {"key": key, "answer": answer}
        self.answers_map = {ans['key']: ans['answer'] for ans in answers}

    def calculate(self) -> dict:
        score = 0
        
        # 1. Income (Max 15)
        income = self.answers_map.get("monthly_income", "")
        if "1,00,000+" in income: score += 15
        elif "50,000" in income: score += 10
        elif "25,000" in income: score += 5
        
        # 2. Expenses Ratio Estimate (Max 15)
        # We don't have the exact ratio easily calculable as numbers since they are strings,
        # but we can do a rough match. For robustness in hackathon, assign flat.
        expenses = self.answers_map.get("monthly_expenses", "")
        if "10,000" in expenses: score += 15
        elif "15,000" in expenses: score += 10
        elif "20,000" in expenses: score += 5
        
        # 3. Savings (Max 15)
        savings = self.answers_map.get("current_savings", "")
        if "20,000+" in savings: score += 15
        elif "10,000" in savings: score += 10
        elif "5,000" in savings: score += 5
        
        # 4. Emergency Fund (Max 15)
        ef = self.answers_map.get("emergency_fund", "")
        if "Yes" in ef: score += 15
        elif "Building" in ef: score += 5
        
        # 5. Experience (Max 20)
        exp = self.answers_map.get("investment_experience", "")
        if "Advanced" in exp: score += 20
        elif "Intermediate" in exp: score += 15
        elif "Beginner" in exp: score += 5
        
        # 6. Risk Tolerance Explicit (Max 20)
        tol = self.answers_map.get("risk_tolerance", "")
        if "High" in tol: score += 20
        elif "Moderate" in tol: score += 10
        
        # Determine Level
        if score <= 30:
            level = "Low"
        elif score <= 70:
            level = "Moderate"
        else:
            level = "High"
            
        return {
            "score": score,
            "level": level
        }
