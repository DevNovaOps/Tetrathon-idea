from django.contrib import admin
from .models import MemoryEntry

@admin.register(MemoryEntry)
class MemoryEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'memory_type', 'title', 'created_at')
    list_filter = ('memory_type',)
    search_fields = ('user__email', 'title', 'summary')
    ordering = ('-created_at',)
