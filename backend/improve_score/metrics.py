from credit_score.metrics import FinancialMetricsCalculator

class ImprovementMetricsGenerator:
    """Calculates success metrics based on current financial profile and potential roadmap."""
    
    def __init__(self, profile, expected_points: int):
        self.profile = profile
        self.metrics = FinancialMetricsCalculator(profile).calculate()
        self.scores = self.metrics.get('scores', {})
        self.expected_points = expected_points

    def generate(self) -> list:
        # Based on the scores calculated by CreditScore's metrics generator
        financial_stability = self.scores.get("financial_stability", 50)
        investment_readiness = self.scores.get("investment_behaviour", 50)
        
        # Risk Reduction: If stability is high, risk reduction is higher (we invert it for presentation)
        risk_reduction = 100 - financial_stability
        if risk_reduction < 10:
            risk_reduction = 10
            
        metrics = []
        
        metrics.append({
            "name": "Expected Credit Improvement",
            "percentage": min(100, int((self.expected_points / 150) * 100)), # arbitrary scale for presentation
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
            "percentage": risk_reduction,
            "value_text": f"-{risk_reduction}% Risk",
            "icon": "⚡",
            "bg_class": "cyan-bg",
            "text_class": "cyan-text",
            "hex_color": "#06B6D4"
        })
        
        return metrics
