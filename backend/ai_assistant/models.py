import uuid
from django.db import models
from accounts.models import User

class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_conversations')
    started_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)
    current_step = models.IntegerField(default=1)
    
    # Final AI outputs
    risk_score = models.IntegerField(null=True, blank=True)
    risk_level = models.CharField(max_length=50, null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    investment_recommendation = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Conversation {self.id} for {self.user.email}"

class ConversationMessage(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    choices = models.JSONField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

class AssessmentAnswer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='answers')
    question_key = models.CharField(max_length=50) # e.g. 'monthly_income', 'risk_tolerance'
    question = models.TextField()
    answer = models.CharField(max_length=255)
    weight = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.question_key}: {self.answer}"
