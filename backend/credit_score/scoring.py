"""
Deterministic Weighted Scoring Engine.
Calculates the final Credit Score and Risk level based on normalized metrics.
"""
import random
from .constants import MIN_SCORE, MAX_SCORE, RISK_LEVELS, METRIC_WEIGHTS

class WeightedScoringEngine:
    """Deterministic scoring engine mapping metrics to a 300-900 score."""

    def __init__(self, metrics: dict):
        self.metrics = metrics
        
    def calculate(self) -> dict:
        """
        Executes the deterministic weighted calculation.
        Returns:
            {
                "credit_score": int (300-900),
                "risk_score": float (0-100),
                "grade": str,
                "category": str,
                "risk_level": str,
                "history": list[int]
            }
        """
        # 1. Calculate Risk Score (0-100) using weighted average
        weighted_sum = 0.0
        for key, weight in METRIC_WEIGHTS.items():
            sub_score = self.metrics.get(key, 0)
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
        
        # 4. Generate deterministic history (synthetic, converging on current score)
        history = self._generate_history(credit_score)

        return {
            "credit_score": credit_score,
            "risk_score": round(risk_score, 2),
            "grade": band["grade"],
            "category": band["category"],
            "risk_level": band["level"],
            "history": history
        }
        
    def _generate_history(self, final_score: int) -> list:
        """Generates a realistic deterministic synthetic history curve."""
        # Using a fixed seed based on the score to keep it deterministic for a given score
        random.seed(final_score)
        
        history = []
        # Start a bit lower and gradually rise to final_score
        current = max(MIN_SCORE, final_score - random.randint(30, 50))
        for _ in range(6):
            history.append(current)
            # increment slowly towards final score
            diff = final_score - current
            current += max(1, int(diff * random.uniform(0.2, 0.5)))
            
        history.append(final_score) # Month 7 is current score
        
        # Reset seed so we don't pollute global random state
        random.seed()
        
        return history
