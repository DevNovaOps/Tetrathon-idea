class RecommendationEngine:
    """
    Generates dynamic personalized action items to improve the risk profile.
    """
    
    @staticmethod
    def generate_recommendations(risk_results: dict) -> list:
        recommendations = []
        subs = risk_results["sub_scores"]
        
        if subs["emergency_fund_strength"] < 50:
            recommendations.append({
                "action": "Increase Emergency Fund",
                "reason": "Your liquid savings cover less than 3 months of expenses.",
                "benefit": "Protects against sudden job loss or medical emergencies.",
                "risk_reduction_estimate": 15,
                "estimated_credit_improvement": 0,
                "estimated_completion_time": "6-12 Months",
                "priority": "High"
            })
            
        if subs["savings_health"] < 50:
            recommendations.append({
                "action": "Increase Monthly Savings",
                "reason": "You are saving less than the recommended 20% of your income.",
                "benefit": "Accelerates wealth accumulation and financial independence.",
                "risk_reduction_estimate": 10,
                "estimated_credit_improvement": 0,
                "estimated_completion_time": "Immediate",
                "priority": "High"
            })
            
        if subs["financial_stability"] < 50:
            recommendations.append({
                "action": "Reduce Discretionary Expenses",
                "reason": "Your monthly expenses are consuming a large portion of your income.",
                "benefit": "Frees up cash flow for investments and debt reduction.",
                "risk_reduction_estimate": 12,
                "estimated_credit_improvement": 5,
                "estimated_completion_time": "1 Month",
                "priority": "Medium"
            })
            
        if subs["behavioral_risk"] < 60:
            recommendations.append({
                "action": "Improve Credit Health",
                "reason": "Your credit score indicates potential borrowing difficulties.",
                "benefit": "Lowers interest rates on future loans.",
                "risk_reduction_estimate": 8,
                "estimated_credit_improvement": 30,
                "estimated_completion_time": "3-6 Months",
                "priority": "Medium"
            })
            
        if risk_results["investment_readiness"] in ["High", "Medium"] and subs["savings_health"] >= 50:
            recommendations.append({
                "action": "Start SIP in Index Funds",
                "reason": "You have a stable surplus and an adequate emergency buffer.",
                "benefit": "Generates long-term compounding returns.",
                "risk_reduction_estimate": 5,
                "estimated_credit_improvement": 0,
                "estimated_completion_time": "Ongoing",
                "priority": "Medium"
            })

        # Ensure at least one fallback recommendation
        if not recommendations:
            recommendations.append({
                "action": "Maintain Current Strategy",
                "reason": "Your financial health is very strong across all metrics.",
                "benefit": "Ensures continued compounding and stability.",
                "risk_reduction_estimate": 0,
                "estimated_credit_improvement": 0,
                "estimated_completion_time": "Ongoing",
                "priority": "Low"
            })

        # Sort by impact
        recommendations = sorted(recommendations, key=lambda x: x["risk_reduction_estimate"], reverse=True)
        return recommendations[:4] # Return top 4
