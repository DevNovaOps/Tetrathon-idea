from .analytics_service import AnalyticsService

class InsightService:
    @staticmethod
    def get_insights(user):
        summary = AnalyticsService.get_summary(user)
        raw = summary["_raw"]
        
        insights = []
        
        # Savings insight
        savings = raw["savings"]
        if savings > 10000:
            insights.append({
                "title": "Your savings have improved over the past 3 months.",
                "description": f"Consistent monthly savings of ₹{savings:,.0f} shows strong financial discipline.",
                "icon": "✓",
                "bg_class": "green-bg"
            })
        else:
            insights.append({
                "title": "Your savings rate has room for improvement.",
                "description": "Consider analyzing your expenses to boost monthly savings.",
                "icon": "⚠",
                "bg_class": "orange-bg"
            })
            
        # Expense insight
        expenses = raw["expenses"]
        if expenses > 40000:
            insights.append({
                "title": "Shopping expenses remain slightly above average.",
                "description": "Consider setting a monthly cap on discretionary shopping.",
                "icon": "⚠",
                "bg_class": "orange-bg"
            })
        else:
            insights.append({
                "title": "Your expenses are well optimized.",
                "description": "Great job keeping discretionary spending under control.",
                "icon": "✓",
                "bg_class": "green-bg"
            })
            
        # Investment insight
        inv = raw["investment_value"]
        if inv > 0:
            insights.append({
                "title": "Your investment consistency is excellent.",
                "description": f"Your portfolio has reached ₹{inv:,.0f}. Keep compounding!",
                "icon": "📈",
                "bg_class": "blue-bg"
            })
        else:
            insights.append({
                "title": "Consider starting an investment portfolio.",
                "description": "Investing early leverages the power of compounding for long-term growth.",
                "icon": "📈",
                "bg_class": "blue-bg"
            })
            
        # Credit Insight
        insights.append({
            "title": "Continue maintaining timely bill payments.",
            "description": "Your on-time payment streak directly boosts your credit score.",
            "icon": "💳",
            "bg_class": "purple-bg"
        })
        
        return insights
