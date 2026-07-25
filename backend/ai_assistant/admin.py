from django.contrib import admin
from .models import Conversation, ConversationMessage, AssessmentAnswer


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'current_step', 'completed', 'risk_score', 'risk_level', 'started_at')
    list_filter = ('completed', 'risk_level')
    search_fields = ('user__email',)


@admin.register(ConversationMessage)
class ConversationMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'role', 'timestamp')
    list_filter = ('role',)


@admin.register(AssessmentAnswer)
class AssessmentAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'question_key', 'answer', 'weight')
