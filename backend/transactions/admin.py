from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'merchant', 'category', 'date', 'is_income', 'source')
    list_filter = ('category', 'is_income', 'source', 'payment_method')
    search_fields = ('user__email', 'merchant', 'description')
    ordering = ('-date',)
