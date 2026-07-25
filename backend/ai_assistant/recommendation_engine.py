"""
Deterministic Investment Recommendation Engine.
Maps risk level to a specific asset allocation.
"""


class RecommendationEngine:
    """Generates investment allocation based on deterministic risk level."""

    ALLOCATIONS = {
        "Low": [
            {"asset": "Debt / Fixed Deposits", "percentage": 70, "color": "#3B82F6"},
            {"asset": "Index Funds", "percentage": 20, "color": "#10B981"},
            {"asset": "Gold / SGBs", "percentage": 10, "color": "#F59E0B"},
        ],
        "Moderate": [
            {"asset": "Index Funds", "percentage": 50, "color": "#10B981"},
            {"asset": "Debt / Fixed Deposits", "percentage": 25, "color": "#3B82F6"},
            {"asset": "Gold / SGBs", "percentage": 15, "color": "#F59E0B"},
            {"asset": "Liquid Funds", "percentage": 10, "color": "#8B5CF6"},
        ],
        "High": [
            {"asset": "Equity / Stocks", "percentage": 70, "color": "#EF4444"},
            {"asset": "Index Funds", "percentage": 20, "color": "#10B981"},
            {"asset": "Crypto / Alternatives", "percentage": 10, "color": "#F59E0B"},
        ],
    }

    @classmethod
    def get_allocation(cls, risk_level: str) -> list:
        """Returns the allocation list for a given risk level."""
        return cls.ALLOCATIONS.get(risk_level, cls.ALLOCATIONS["Moderate"])
