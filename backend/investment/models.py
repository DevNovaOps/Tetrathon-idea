import uuid
from django.db import models
from accounts.models import User

class InvestmentProfile(models.Model):
    """Core investment profile containing summary data."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='investment_profile')
    
    # Financial metrics
    monthly_sip = models.IntegerField(default=0)
    target_value = models.IntegerField(default=0)
    horizon_years = models.IntegerField(default=5)
    expected_cagr = models.CharField(max_length=20, default="10-12%")
    confidence_score = models.IntegerField(default=0)
    risk_bucket = models.CharField(max_length=50, blank=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'investment_profiles'


class PortfolioAsset(models.Model):
    """Specific asset allocation for the user."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(InvestmentProfile, on_delete=models.CASCADE, related_name='assets')
    
    name = models.CharField(max_length=100) # Index Fund, Debt Fund, etc.
    allocation_pct = models.IntegerField()
    expected_cagr_range = models.CharField(max_length=20) # e.g. "10-12%"
    risk_level = models.CharField(max_length=50) # Moderate, Low
    is_highly_recommended = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'investment_assets'
        ordering = ['-allocation_pct']


class InvestmentGuidance(models.Model):
    """AI recommendations for portfolio management."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(InvestmentProfile, on_delete=models.CASCADE, related_name='guidance')
    
    action = models.CharField(max_length=200)
    reason = models.TextField()
    color_theme = models.CharField(max_length=50, default="green") # UI color mapping
    
    class Meta:
        db_table = 'investment_guidance'


class PortfolioBenefit(models.Model):
    """Dynamically generated key benefits of the allocation."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(InvestmentProfile, on_delete=models.CASCADE, related_name='benefits')
    
    title = models.CharField(max_length=100)
    description = models.TextField()
    color_theme = models.CharField(max_length=50, default="green")
    emoji = models.CharField(max_length=10, default="🛡️")
    
    class Meta:
        db_table = 'investment_benefits'
