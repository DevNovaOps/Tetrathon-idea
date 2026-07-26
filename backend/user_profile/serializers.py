from rest_framework import serializers
from .models import (
    UserProfile, FinancialGoal, GoalContribution, ConnectedBank,
    ConnectedUPI, ConnectedCard, UserTimeline, ExplainabilityHistory,
    FinancialSnapshotHistory
)

class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    display_name = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            'id', 'full_name', 'profile_picture', 'phone', 'email',
            'date_of_birth', 'gender', 'occupation', 'education',
            'address', 'city', 'state', 'country', 'preferred_language',
            'preferred_currency', 'time_zone', 'completion_percentage',
            'display_name', 'created_at', 'updated_at'
        ]

    def get_email(self, obj):
        return obj.email or (obj.user.email if obj.user else "")

    def get_display_name(self, obj):
        if obj.full_name:
            return obj.full_name
        return obj.user.email.split('@')[0] if obj.user else ""


class GoalContributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoalContribution
        fields = ['id', 'goal', 'amount', 'date', 'notes', 'created_at']


class FinancialGoalSerializer(serializers.ModelSerializer):
    contributions = GoalContributionSerializer(many=True, read_only=True)
    deadline_formatted = serializers.SerializerMethodField()

    class Meta:
        model = FinancialGoal
        fields = [
            'id', 'goal_name', 'goal_type', 'target_amount', 'current_progress',
            'monthly_contribution', 'deadline', 'deadline_formatted',
            'priority', 'status', 'is_primary', 'completion_percentage',
            'contributions', 'created_at', 'updated_at'
        ]

    def get_deadline_formatted(self, obj):
        if obj.deadline:
            return obj.deadline.strftime("%B %Y")
        return "No Deadline"


class ConnectedBankSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectedBank
        fields = [
            'id', 'bank_name', 'masked_account', 'ifsc', 'account_type',
            'verified', 'connection_status', 'created_at'
        ]


class ConnectedUPISerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectedUPI
        fields = ['id', 'upi_id', 'upi_app', 'verification_status', 'created_at']


class ConnectedCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectedCard
        fields = [
            'id', 'card_type', 'issuer', 'card_holder', 'last_4_digits',
            'masked_number', 'expiry', 'status', 'credit_limit',
            'billing_date', 'due_date', 'created_at'
        ]


class UserTimelineSerializer(serializers.ModelSerializer):
    time_ago = serializers.SerializerMethodField()
    date_formatted = serializers.SerializerMethodField()

    class Meta:
        model = UserTimeline
        fields = [
            'id', 'event_type', 'title', 'description', 'category',
            'metadata', 'created_at', 'time_ago', 'date_formatted'
        ]

    def get_time_ago(self, obj):
        from django.utils import timezone
        now = timezone.now()
        diff = now - obj.created_at
        seconds = diff.total_seconds()
        if seconds < 60:
            return "Just now"
        elif seconds < 3600:
            mins = int(seconds // 60)
            return f"{mins}m ago"
        elif seconds < 86400:
            hours = int(seconds // 3600)
            return f"{hours}h ago"
        else:
            days = int(seconds // 86400)
            return f"{days}d ago"

    def get_date_formatted(self, obj):
        return obj.created_at.strftime("%b %d, %Y")


class ExplainabilityHistorySerializer(serializers.ModelSerializer):
    date_formatted = serializers.SerializerMethodField()

    class Meta:
        model = ExplainabilityHistory
        fields = ['id', 'summary_text', 'reference_data', 'created_at', 'date_formatted']

    def get_date_formatted(self, obj):
        return obj.created_at.strftime("%B %d, %Y")


class FinancialSnapshotHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialSnapshotHistory
        fields = [
            'id', 'credit_score', 'risk_profile', 'monthly_income',
            'monthly_savings', 'investment_portfolio', 'net_worth',
            'financial_health_score', 'recorded_at'
        ]
