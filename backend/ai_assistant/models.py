import uuid
from django.db import models
from accounts.models import User


class Conversation(models.Model):
    """Stores a single AI assessment conversation session per user."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_conversations')
    current_step = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    risk_score = models.IntegerField(null=True, blank=True)
    risk_level = models.CharField(max_length=20, blank=True, default='')
    summary = models.TextField(blank=True, default='')
    started_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f"Conversation {self.id} - Step {self.current_step}"


class ConversationMessage(models.Model):
    """Individual chat messages within a conversation."""
    ROLE_CHOICES = [('assistant', 'Assistant'), ('user', 'User')]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.role}: {self.content[:50]}"


class AssessmentAnswer(models.Model):
    """Stores each individual answer to an assessment question."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='answers')
    question_key = models.CharField(max_length=50)
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    numeric_value = models.IntegerField(null=True, blank=True)
    weight = models.FloatField(default=1.0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.question_key}: {self.answer}"
