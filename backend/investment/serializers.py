from rest_framework import serializers
from .models import InvestmentProfile, PortfolioAsset, InvestmentGuidance, PortfolioBenefit

class PortfolioAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioAsset
        fields = ['name', 'allocation_pct', 'expected_cagr_range', 'risk_level', 'is_highly_recommended']

class InvestmentGuidanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentGuidance
        fields = ['action', 'reason', 'color_theme']

class PortfolioBenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioBenefit
        fields = ['title', 'description', 'color_theme', 'emoji']

class InvestmentProfileSerializer(serializers.ModelSerializer):
    allocation = PortfolioAssetSerializer(source='assets', many=True, read_only=True)
    ai_recommendations = InvestmentGuidanceSerializer(source='guidance', many=True, read_only=True)
    portfolio_benefits = PortfolioBenefitSerializer(source='benefits', many=True, read_only=True)
    
    educational_disclaimer = serializers.SerializerMethodField()
    scenarios = serializers.SerializerMethodField()

    
    class Meta:
        model = InvestmentProfile
        fields = [
            'monthly_sip', 'target_value', 'horizon_years', 'expected_cagr', 
            'confidence_score', 'risk_bucket', 'allocation', 'ai_recommendations', 
            'portfolio_benefits', 'educational_disclaimer', 'scenarios'
        ]
        
    def get_educational_disclaimer(self, obj):
        from config.disclaimers import EDUCATIONAL_DISCLAIMER
        return EDUCATIONAL_DISCLAIMER

    def get_scenarios(self, obj):
        from .allocation_engine import AllocationEngine
        from risk_profile.financial_snapshot_service import FinancialSnapshotService
        snapshot = FinancialSnapshotService.generate_snapshot(obj.user)
        return AllocationEngine.generate_multi_scenario_allocation(obj.risk_bucket, snapshot)
