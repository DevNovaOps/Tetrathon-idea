from ai_assistant.groq_client import GroqService

class AIGuidanceEngine:
    
    @staticmethod
    def generate_guidance(snapshot: dict, risk_results: dict, allocation: list) -> list:
        guidance = []
        
        # 1. SIP Discipline
        guidance.append({
            "action": "Maintain monthly SIP discipline",
            "reason": "Automate monthly SIP transfers on the 1st of every month for compound growth.",
            "color": "green"
        })
        
        # 2. Risk Specific
        if risk_results["risk_bucket"] == "High":
            guidance.append({
                "action": "Monitor High-Equity Exposure",
                "reason": "Your portfolio has significant equity. Prepare for short-term volatility in exchange for long-term gains.",
                "color": "purple"
            })
        else:
            guidance.append({
                "action": "Avoid unverified high-risk assets",
                "reason": "Steer clear of speculative crypto or penny stocks to preserve capital security.",
                "color": "purple"
            })
            
        # 3. Step up
        guidance.append({
            "action": "Step-up SIP as monthly income grows",
            "reason": "Increase monthly investment by 10% annually with every salary raise.",
            "color": "orange"
        })
        
        # 4. Review
        guidance.append({
            "action": "Review portfolio every 6 months",
            "reason": "Rebalance asset classes if equity exceeds 50% due to market fluctuations.",
            "color": "blue"
        })
        
        return guidance

    @staticmethod
    def generate_benefits(allocation: list) -> list:
        # Based on allocation, generate benefits
        benefits = [
            {"title": "Diversification", "desc": "Spread across equities, debt, gold, and cash equivalents.", "color": "green", "emoji": "🛡️"},
            {"title": "Lower Volatility", "desc": "Debt and liquid funds act as a shock absorber during market pullbacks.", "color": "blue", "emoji": "📉"},
            {"title": "Long-Term Growth", "desc": "Index funds & Blue Chips capture compounding equity market gains.", "color": "purple", "emoji": "🚀"},
            {"title": "High Liquidity", "desc": "Liquid fund reserves ensure immediate access to funds within 24 hours.", "color": "cyan", "emoji": "💧"},
            {"title": "Stable Returns", "desc": "Consistent average annual return target across cycles.", "color": "orange", "emoji": "⚖️"},
            {"title": "Inflation Protection", "desc": "Gold ETFs and index funds hedge against purchasing power erosion.", "color": "green", "emoji": "📈"}
        ]
        return benefits
