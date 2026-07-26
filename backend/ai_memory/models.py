"""
AI Memory models — unified memory layer for Explainable AI.
"""
import uuid
from django.db import models
from django.conf import settings


MEMORY_TYPE_CHOICES = [
    ('risk_change', 'Risk Profile Change'),
    ('goal_progress', 'Goal Progress'),
    ('goal_completed', 'Goal Completed'),
    ('credit_change', 'Credit Score Change'),
    ('investment_update', 'Investment Update'),
    ('learning_milestone', 'Learning Milestone'),
    ('transaction_pattern', 'Transaction Pattern'),
    ('behavior_change', 'Behaviour Change'),
    ('budget_update', 'Budget Update'),
    ('conversation_summary', 'AI Conversation Summary'),
    ('notification_event', 'Notification Event'),
    ('digital_signal_update', 'Digital Signal Update'),
]


class MemoryEntry(models.Model):
    """
    Single unit of AI memory.
    Stores a fact, event, or observation about the user's financial journey.
    Referenced by Explainable AI to generate data-backed explanations.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ai_memories'
    )
    memory_type = models.CharField(max_length=50, choices=MEMORY_TYPE_CHOICES, db_index=True)
    title = models.CharField(max_length=255)
    summary = models.TextField()
    data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'ai_memory_entries'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'memory_type']),
            models.Index(fields=['user', 'created_at']),
        ]

    def __str__(self):
        return f"[{self.memory_type}] {self.title} — {self.user.email}"
