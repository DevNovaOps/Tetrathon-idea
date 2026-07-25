from credit_score.metrics import FinancialMetricsCalculator

class ImprovementMetricsGenerator:
    """Calculates dynamic success metrics based on current financial profile and potential roadmap."""
    
    def __init__(self, profile, expected_points: int):
        self.profile = profile
        self.metrics = FinancialMetricsCalculator(profile).calculate()
        self.scores = self.metrics.get('scores', {})
        self.raw = self.metrics.get('raw', {})
        self.expected_points = expected_points

    def generate(self) -> list:
        # Dynamic calculations based on Credit Score metrics engine
        financial_stability = self.scores.get("financial_stability", 50)
        investment_readiness = self.scores.get("investment_behaviour", 50)
        
        # Risk Reduction: Base risk is inverted stability and payment behavior
        payment_behaviour = self.scores.get("payment_behaviour", 50)
        base_risk = 100 - ((financial_stability + payment_behaviour) / 2)
        # Expected risk reduction based on completing the plan (assuming +20% improvement)
        risk_reduction = min(base_risk, 20 + int(self.expected_points * 0.2))
        
        # Savings Health
        savings_ratio = self.raw.get("savings_ratio", 0)
        if savings_ratio >= 6:
            savings_status = "Excellent"
        elif savings_ratio >= 3:
            savings_status = "Good"
        elif savings_ratio > 1:
            savings_status = "Fair"
        else:
            savings_status = "Poor"
            
        metrics = []
        
        metrics.append({
            "name": "Expected Credit Improvement",
            "percentage": min(100, int((self.expected_points / 150) * 100)), # Max 150 points scale for progress bar
            "value_text": f"+{self.expected_points} Pts",
            "icon": "📈",
            "bg_class": "green-bg",
            "text_class": "green-text",
            "hex_color": "#10B981"
        })
        
        metrics.append({
            "name": "Financial Stability Score",
            "percentage": financial_stability,
            "value_text": f"{financial_stability} / 100",
            "icon": "🛡️",
            "bg_class": "blue-bg",
            "text_class": "blue-text",
            "hex_color": "#3B82F6"
        })
        
        metrics.append({
            "name": "Investment Readiness",
            "percentage": investment_readiness,
            "value_text": "High" if investment_readiness > 75 else "Medium" if investment_readiness > 40 else "Low",
            "icon": "💎",
            "bg_class": "purple-bg",
            "text_class": "purple-text",
            "hex_color": "#A855F7"
        })
        
        metrics.append({
            "name": "Risk Profile Reduction",
            "percentage": int(risk_reduction),
            "value_text": f"-{int(risk_reduction)}% Risk",
            "icon": "⚡",
            "bg_class": "cyan-bg",
            "text_class": "cyan-text",
            "hex_color": "#06B6D4"
        })
        
        metrics.append({
            "name": "Savings Health",
            "percentage": min(100, int(savings_ratio * 16.66)), # 6 months = 100%
            "value_text": savings_status,
            "icon": "🏦",
            "bg_class": "emerald-bg",
            "text_class": "emerald-text",
            "hex_color": "#059669"
        })
        
        return metrics
