"""Admin registration for the User model."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom admin for the User model."""

    list_display = ('email', 'full_name', 'auth_provider', 'onboarding_completed', 'is_active', 'date_joined')
    list_filter = ('auth_provider', 'is_active', 'is_staff', 'onboarding_completed')
    search_fields = ('email', 'full_name', 'phone')
    ordering = ('-date_joined',)
    readonly_fields = ('id', 'date_joined', 'created_at', 'updated_at')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'phone', 'country')}),
        ('OAuth', {'fields': ('auth_provider', 'google_id', 'profile_picture')}),
        ('Status', {'fields': ('is_verified', 'is_active', 'is_staff', 'is_superuser', 'onboarding_completed')}),
        ('Timestamps', {'fields': ('id', 'date_joined', 'created_at', 'updated_at')}),
        ('Permissions', {'fields': ('groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2'),
        }),
    )
