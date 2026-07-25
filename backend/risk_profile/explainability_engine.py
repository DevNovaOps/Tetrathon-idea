from ai_assistant.groq_client import GroqService

class ExplainabilityEngine:
    """
    Deterministically identifies feature impact and explains the risk score.
    """
    
    @staticmethod
    def generate_explanations(risk_results: dict, features: list) -> dict:
        positive = []
        negative = []
        
        for f in features:
            if f["impact"] > 0:
                positive.append({
                    "feature": f["feature"],
                    "impact": f["impact"],
                    "reason": f"Significant positive impact (+{f['impact']}) on overall risk profile."
                })
            elif f["impact"] < 0:
                negative.append({
                    "feature": f["feature"],
                    "impact": f["impact"],
                    "reason": f"Negative impact ({f['impact']}) requiring attention."
                })
                
        # Already sorted by magnitude from feature_importance, but let's take top 3
        positive = positive[:3]
        # For negative, sort by impact ascending (most negative first)
        negative = sorted(negative, key=lambda x: x["impact"])[:3]

        # Generate a prompt for Groq to write a natural language summary
        score = risk_results["risk_score"]
        bucket = risk_results["risk_bucket"]
        
        prompt = f"""
        Generate a 2-sentence financial risk explanation for the user.
        Their risk score is {score}/100, which falls into the '{bucket}' bucket.
        Top positive factor: {positive[0]['feature'] if positive else 'None'}.
        Top negative factor: {negative[0]['feature'] if negative else 'None'}.
        Use a warm, professional, encouraging tone. Do not use bullet points.
        """
        
        try:
            ai_explanation = GroqService.chat(prompt)
        except Exception:
            ai_explanation = f"Your financial profile reflects a {bucket} risk level. Keep optimizing your top areas to improve your financial resilience."

        return {
            "positive_factors": positive,
            "negative_factors": negative,
            "ai_explanation": ai_explanation
        }
