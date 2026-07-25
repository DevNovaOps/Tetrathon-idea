class RecommendationEngine:
    """
    Generates deterministic investment allocation based on the calculated risk level.
    """
    def __init__(self, risk_level: str):
        self.risk_level = risk_level

    def generate(self) -> dict:
        if self.risk_level == "Low":
            return {
                "allocation": [
                    {"name": "Debt Funds", "percentage": 70},
                    {"name": "Index Funds", "percentage": 20},
                    {"name": "Gold", "percentage": 10}
                ]
            }
        elif self.risk_level == "Moderate":
            return {
                "allocation": [
                    {"name": "Index Funds", "percentage": 50},
                    {"name": "Debt Funds", "percentage": 25},
                    {"name": "Gold", "percentage": 15},
                    {"name": "Liquid Funds", "percentage": 10}
                ]
            }
        else: # High
            return {
                "allocation": [
                    {"name": "Equity (Direct)", "percentage": 70},
                    {"name": "Index Funds", "percentage": 20},
                    {"name": "Crypto/Alternatives", "percentage": 10}
                ]
            }
