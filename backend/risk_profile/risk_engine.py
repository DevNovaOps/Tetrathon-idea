class RiskEngine:
    """
    Deterministic Financial Risk Calculator.
    Calculates exact risk scores, buckets, and sub-metrics based on snapshot data.
    """
    
    @staticmethod
    def calculate(snapshot: dict) -> dict:
        income = float(snapshot.get("monthly_income", 0))
        expenses = float(snapshot.get("monthly_expenses", 0))
        savings = float(snapshot.get("monthly_savings", 0))
        credit_score = int(snapshot.get("credit_score", 0))
        emergency_status = str(snapshot.get("emergency_fund_status", "")).lower()
        
        # 1. Base Calculations
        surplus = max(0, income - expenses)
        savings_rate = (savings / income * 100) if income > 0 else 0
        expense_ratio = (expenses / income * 100) if income > 0 else 100
        
        # Emergency Fund Numeric Approximation based on text status
        if "yes" in emergency_status:
            ef_months = 6.0
        elif "building" in emergency_status:
            ef_months = 2.0
        else:
            ef_months = 0.0
            
        emergency_coverage = ef_months # already in months

        # 2. Sub-metric Scoring (0-100 scales)
        # Savings Health
        if savings_rate >= 30:
            savings_health = 100
        elif savings_rate >= 20:
            savings_health = 75
        elif savings_rate >= 10:
            savings_health = 50
        else:
            savings_health = 25
            
        # Financial Stability (Expense Ratio based)
        if expense_ratio <= 50:
            stability = 100
        elif expense_ratio <= 70:
            stability = 75
        elif expense_ratio <= 90:
            stability = 40
        else:
            stability = 10

        # Behavioral Risk (Credit Score proxy)
        if credit_score >= 750:
            behavior = 100
        elif credit_score >= 650:
            behavior = 70
        elif credit_score >= 550:
            behavior = 40
        elif credit_score > 0:
            behavior = 20
        else:
            behavior = 50 # Default if no credit score

        # Emergency Fund Strength
        if emergency_coverage >= 6:
            ef_strength = 100
        elif emergency_coverage >= 3:
            ef_strength = 75
        elif emergency_coverage > 0:
            ef_strength = 40
        else:
            ef_strength = 0
            
        # Investment Readiness
        # Need high stability, good emergency fund, and positive surplus
        readiness_pct = int(min(100, max(0, (stability * 0.4) + (ef_strength * 0.4) + (savings_health * 0.2))))
        
        if readiness_pct >= 80:
            readiness = "High"
            readiness_reason = "Strong surplus and excellent emergency savings make you fully ready for investments."
        elif readiness_pct >= 50:
            readiness = "Moderately Ready"
            readiness_reason = "Stable finances, but consider strengthening your emergency buffer before aggressive investing."
        else:
            readiness = "Low"
            readiness_reason = "Focus on building an emergency fund and consistent savings before investing."

        # 3. Final Risk Score Calculation (0-100)
        # Higher score = Lower Risk (Better financial health)
        weighted_score = (
            (savings_health * 0.25) +
            (stability * 0.25) +
            (behavior * 0.25) +
            (ef_strength * 0.25)
        )
        
        risk_score = int(max(0, min(100, weighted_score)))
        
        # 4. Buckets
        if risk_score >= 70:
            bucket = "Low"
        elif risk_score >= 40:
            bucket = "Moderate"
        else:
            bucket = "High"
            
        # 5. Confidence Estimation
        data_points = [income > 0, expenses > 0, savings > 0, credit_score > 0, bool(emergency_status)]
        confidence = int((sum(data_points) / len(data_points)) * 100)
        
        return {
            "savings_rate": savings_rate,
            "expense_ratio": expense_ratio,
            "monthly_surplus": surplus,
            "emergency_coverage": emergency_coverage,
            "sub_scores": {
                "savings_health": savings_health,
                "financial_stability": stability,
                "behavioral_risk": behavior,
                "emergency_fund_strength": ef_strength
            },
            "investment_readiness": readiness,
            "investment_readiness_pct": readiness_pct,
            "investment_readiness_reason": readiness_reason,
            "risk_score": risk_score,
            "risk_bucket": bucket,
            "confidence_score": confidence
        }
