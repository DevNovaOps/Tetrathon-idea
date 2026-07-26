from django.contrib import admin
from .models import DigitalSignalProfile

@admin.register(DigitalSignalProfile)
class DigitalSignalProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'electricity_bill_frequency', 'upi_transaction_frequency', 'updated_at')
    search_fields = ('user__email',)
