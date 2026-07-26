import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone

class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_profile')
    full_name = models.CharField(max_length=150, blank=True)
    profile_picture = models.URLField(max_length=500, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=30, blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    education = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default='India', blank=True)
    preferred_language = models.CharField(max_length=50, default='English', blank=True)
    preferred_currency = models.CharField(max_length=10, default='INR', blank=True)
    time_zone = models.CharField(max_length=50, default='Asia/Kolkata', blank=True)
    completion_percentage = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile for {self.user.email} ({self.completion_percentage}%)"


class FinancialGoal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='financial_goals')
    goal_name = models.CharField(max_length=150)
    goal_type = models.CharField(max_length=50, default='Custom')
    target_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    current_progress = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    monthly_contribution = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    deadline = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=20, default='Medium')
    status = models.CharField(max_length=20, default='Active')  # Active, Completed, Paused, Cancelled
    is_primary = models.BooleanField(default=False)  # The ONE active primary simulator goal
    completion_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_primary', '-created_at']

    def __str__(self):
        return f"{self.goal_name} ({self.status}) - {self.user.email}"


class GoalContribution(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    goal = models.ForeignKey(FinancialGoal, on_delete=models.CASCADE, related_name='contributions')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateField(default=timezone.now)
    notes = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"₹{self.amount} to {self.goal.goal_name}"


class ConnectedBank(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='connected_banks')
    bank_name = models.CharField(max_length=100)
    masked_account = models.CharField(max_length=30)
    ifsc = models.CharField(max_length=20, blank=True)
    account_type = models.CharField(max_length=50, default='Savings')
    verified = models.BooleanField(default=True)
    connection_status = models.CharField(max_length=20, default='Active')
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bank_name} ({self.masked_account})"


class ConnectedUPI(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='connected_upis')
    upi_id = models.CharField(max_length=100)
    upi_app = models.CharField(max_length=50, default='Google Pay')
    verification_status = models.CharField(max_length=20, default='Verified')
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.upi_id} via {self.upi_app}"


class ConnectedCard(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='connected_cards')
    card_type = models.CharField(max_length=20, default='Debit')  # Debit or Credit
    issuer = models.CharField(max_length=100, default='HDFC Bank')
    card_holder = models.CharField(max_length=150, blank=True)
    last_4_digits = models.CharField(max_length=4)
    masked_number = models.CharField(max_length=30, blank=True)
    expiry = models.CharField(max_length=10, blank=True)
    status = models.CharField(max_length=20, default='Active')
    credit_limit = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    billing_date = models.IntegerField(null=True, blank=True)
    due_date = models.IntegerField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.issuer} {self.card_type} ending {self.last_4_digits}"


class UserTimeline(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='timeline_events')
    event_type = models.CharField(max_length=50, db_index=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, default='General')
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.event_type}] {self.title} for {self.user.email}"


class ExplainabilityHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='explainability_history')
    summary_text = models.TextField()
    reference_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Explainability Summary ({self.created_at.strftime('%Y-%m-%d')})"


class FinancialSnapshotHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='snapshot_history')
    credit_score = models.IntegerField(default=700)
    risk_profile = models.CharField(max_length=50, default='Moderate')
    monthly_income = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    monthly_savings = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    investment_portfolio = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    net_worth = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    financial_health_score = models.IntegerField(default=75)
    recorded_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-recorded_at']

    def __str__(self):
        return f"Snapshot for {self.user.email} at {self.recorded_at.strftime('%Y-%m-%d')}"
