"""Admin registration for the UserProfile model."""
from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin view for UserProfile."""

    list_display = (
        'user',
        'current_step',
        'step1_completed',
        'step2_completed',
        'step3_completed',
        'onboarding_completed',
        'updated_at',
    )
    list_filter = ('onboarding_completed', 'current_step', 'gender', 'preferred_language')
    search_fields = ('user__email', 'user__full_name', 'full_name', 'city')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Step 1 — Personal', {
            'fields': ('full_name', 'age', 'gender', 'occupation', 'city', 'preferred_language'),
        }),
        ('Step 2 — Financial', {
            'fields': (
                'monthly_income', 'monthly_expenses', 'savings',
                'existing_loans', 'upi_usage', 'bill_payment_habit',
            ),
        }),
        ('Step 3 — Investment', {
            'fields': (
                'investment_experience', 'emergency_fund', 'monthly_investment_budget',
                'financial_goal', 'risk_preference', 'investment_duration',
            ),
        }),
        ('Progress', {
            'fields': (
                'current_step', 'step1_completed', 'step2_completed',
                'step3_completed', 'onboarding_completed',
            ),
        }),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
