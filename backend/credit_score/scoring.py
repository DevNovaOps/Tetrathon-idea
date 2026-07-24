"""
Deterministic Weighted Scoring Engine.
Calculates the final Credit Score and Risk level based on normalized metrics.
"""
from .constants import MIN_SCORE, MAX_SCORE, RISK_LEVELS, METRIC_WEIGHTS

class WeightedScoringEngine:
    """Deterministic scoring engine mapping metrics to a 300-900 score."""

    def __init__(self, metrics_data: dict):
        self.raw = metrics_data.get("raw", {})
        self.scores = metrics_data.get("scores", {})
        
    def calculate(self) -> dict:
        """
        Executes the deterministic weighted calculation.
        Returns:
            {
                "credit_score": int (300-900),
                "risk_score": float (0-100),
                "grade": str,
                "category": str,
                "risk_level": str
            }
        """
        # 1. Calculate Risk Score (0-100) using weighted average
        weighted_sum = 0.0
        for key, weight in METRIC_WEIGHTS.items():
            sub_score = self.scores.get(key, 0)
            weighted_sum += (sub_score * weight)
            
        risk_score = min(100.0, max(0.0, weighted_sum))
        
        # 2. Map to Credit Score (300-900)
        score_range = MAX_SCORE - MIN_SCORE
        credit_score = int(MIN_SCORE + (risk_score / 100.0) * score_range)
        
        # 3. Determine Tier/Band
        band = next(
            (r for r in RISK_LEVELS if r["min"] <= credit_score <= r["max"]),
            RISK_LEVELS[-1] # fallback to highest if somehow exceeded
        )

        return {
            "credit_score": credit_score,
            "risk_score": round(risk_score, 2),
            "grade": band["grade"],
            "category": band["category"],
            "risk_level": band["level"]
        }
