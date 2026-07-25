from rest_framework import serializers
from .models import RiskProfile, RiskFeature, RiskRecommendation, RiskHistory

class RiskFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskFeature
        fields = ['feature_name', 'impact', 'reason', 'is_positive']


class RiskRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskRecommendation
        fields = ['action', 'reason', 'benefit', 'risk_reduction_estimate', 'estimated_credit_improvement', 'estimated_completion_time', 'priority']


class RiskHistorySerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(source='assessment_timestamp', format="%Y-%m-%d")
    
    class Meta:
        model = RiskHistory
        fields = ['previous_score', 'current_score', 'previous_bucket', 'current_bucket', 'timestamp']


class RiskProfileSerializer(serializers.ModelSerializer):
    ai_summary = serializers.SerializerMethodField()
    feature_importance = serializers.SerializerMethodField()
    risk_breakdown = serializers.SerializerMethodField()
    investment_readiness = serializers.SerializerMethodField()
    portfolio_allocation = serializers.JSONField()
    recommendations = RiskRecommendationSerializer(many=True, read_only=True)
    history = serializers.SerializerMethodField()
    educational_disclaimer = serializers.SerializerMethodField()
    
    class Meta:
        model = RiskProfile
        fields = [
            'risk_score', 'risk_bucket', 'confidence_score', 'investment_readiness',
            'feature_importance', 'portfolio_allocation', 'risk_breakdown', 
            'ai_summary', 'recommendations', 'history', 'educational_disclaimer'
        ]

    def get_ai_summary(self, obj):
        pos_features = obj.features.filter(is_positive=True)[:3]
        neg_features = obj.features.filter(is_positive=False)[:3]
        return {
            "positive_factors": [f.feature_name for f in pos_features],
            "negative_factors": [f.feature_name for f in neg_features],
            "natural_language_explanation": obj.ai_risk_explanation
        }

    def get_feature_importance(self, obj):
        features = obj.features.all()
        return [{"feature": f.feature_name, "impact": f.impact} for f in features]
        
    def get_risk_breakdown(self, obj):
        """Generates dynamic breakdown items for the UI (Percentage + Status)."""
        savings_pct = int(min(100, max(0, obj.savings_rate_pct or 0)))
        ef_pct = int(min(100, max(0, (obj.emergency_coverage_months or 0) / 6 * 100)))
        discipline_pct = int(min(100, max(0, 100 - (obj.expense_ratio_pct or 100))))
        
        return [
            {"title": "Income Stability", "percentage": 86, "status": "High", "color": "green", "emoji": "💼"},
            {"title": "Savings Habit", "percentage": savings_pct, "status": "Good" if savings_pct >= 20 else "Average", "color": "blue", "emoji": "🏦"},
            {"title": "Emergency Fund", "percentage": ef_pct, "status": "Available" if (obj.emergency_coverage_months or 0) >= 3 else "Needs Work", "color": "green", "emoji": "🛡️"},
            {"title": "Risk Capacity", "percentage": obj.risk_score, "status": obj.risk_bucket, "color": "orange", "emoji": "⚡"},
            {"title": "Financial Discipline", "percentage": discipline_pct, "status": "Good" if (obj.expense_ratio_pct or 100) <= 70 else "Needs Work", "color": "cyan", "emoji": "✅"}
        ]

    def get_investment_readiness(self, obj):
        return {
            "percentage": obj.investment_readiness_pct,
            "readiness_level": obj.investment_readiness,
            "reason": obj.investment_readiness_reason,
            "next_action": "Proceed with tailored investment allocation." if obj.investment_readiness_pct >= 50 else "Focus on building savings first."
        }

    def get_history(self, obj):
        history = RiskHistory.objects.filter(user=obj.user).order_by('-assessment_timestamp')[:5]
        return RiskHistorySerializer(history, many=True).data
        
    def get_educational_disclaimer(self, obj):
        return "This assessment is generated for educational purposes only and does not constitute regulated financial advice."
