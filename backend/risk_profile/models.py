import uuid
from django.db import models
from django.conf import settings


class RiskProfile(models.Model):
    """
    Centralized Financial Snapshot & Risk Profile.
    Single Source of Truth for the user's risk assessment.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='risk_profile'
    )
    
    # Snapshot Metrics (cached from Profile/CreditScore/ImproveScore to avoid N+1 queries)
    monthly_income = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    monthly_expenses = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    monthly_savings = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    savings_rate_pct = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    expense_ratio_pct = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    monthly_surplus = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    emergency_coverage_months = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Engine Results
    risk_score = models.IntegerField(null=True, blank=True)
    risk_bucket = models.CharField(max_length=50, blank=True, default='') # High, Moderate, Low
    confidence_score = models.IntegerField(default=0) # 0-100%
    investment_readiness = models.CharField(max_length=50, blank=True, default='') # Low, Medium, High
    investment_readiness_pct = models.IntegerField(default=0)
    investment_readiness_reason = models.TextField(blank=True, default='')
    portfolio_allocation = models.JSONField(null=True, blank=True)
    
    # AI Explainability Context
    ai_risk_explanation = models.TextField(blank=True, default='')
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'risk_profiles'

    def __str__(self):
        return f"RiskProfile for {self.user.email} - Score: {self.risk_score}"


class RiskFeature(models.Model):
    """Stores deterministic top positive and negative factors affecting the score."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    risk_profile = models.ForeignKey(RiskProfile, on_delete=models.CASCADE, related_name='features')
    
    feature_name = models.CharField(max_length=100) # e.g. "Savings Rate", "Expense Ratio"
    impact = models.IntegerField() # Positive or negative number
    reason = models.TextField() # e.g. "Healthy savings discipline."
    is_positive = models.BooleanField() # True if impact > 0
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'risk_features'
        ordering = ['-is_positive', '-impact']


class RiskRecommendation(models.Model):
    """Dynamically generated actionable steps."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    risk_profile = models.ForeignKey(RiskProfile, on_delete=models.CASCADE, related_name='recommendations')
    
    action = models.CharField(max_length=255) # e.g. "Increase Savings"
    reason = models.TextField()
    benefit = models.TextField()
    risk_reduction_estimate = models.IntegerField(default=0) # e.g. +5 pts
    estimated_credit_improvement = models.IntegerField(null=True, blank=True) # e.g. +10 pts
    estimated_completion_time = models.CharField(max_length=50, blank=True, default='')
    priority = models.CharField(max_length=20) # High, Medium, Low
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'risk_recommendations'
        ordering = ['-risk_reduction_estimate']


class RiskHistory(models.Model):
    """Immutable audit log of historical risk scores."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='risk_history'
    )
    
    previous_score = models.IntegerField(null=True, blank=True)
    current_score = models.IntegerField()
    previous_bucket = models.CharField(max_length=50, blank=True, default='')
    current_bucket = models.CharField(max_length=50)
    
    assessment_timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'risk_history'
        ordering = ['-assessment_timestamp']

    def __str__(self):
        return f"{self.user.email} - {self.previous_score} -> {self.current_score}"
