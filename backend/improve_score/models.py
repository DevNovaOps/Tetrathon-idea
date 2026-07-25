import uuid
from django.db import models
from accounts.models import User

class ImprovementPlan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='improvement_plan')
    current_score = models.IntegerField()
    estimated_score = models.IntegerField()
    target_score = models.IntegerField()
    completion_percentage = models.FloatField(default=0.0)
    estimated_days = models.IntegerField(default=60)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Plan for {self.user.email} - {self.completion_percentage}%"

class ImprovementTask(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plan = models.ForeignKey(ImprovementPlan, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField()
    reason = models.TextField(default='')
    benefit = models.TextField(default='')
    priority = models.CharField(max_length=50) # e.g., 'Critical', 'High', 'Medium', 'Low'
    expected_points = models.IntegerField()
    difficulty = models.CharField(max_length=50) # e.g., 'Easy', 'Medium', 'Hard'
    duration = models.CharField(max_length=50) # e.g., '30 Days', 'Immediate'
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    order = models.IntegerField(default=0)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['order', 'created_at']

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.priority})"

class WeeklyRoadmap(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plan = models.ForeignKey(ImprovementPlan, on_delete=models.CASCADE, related_name='roadmap_weeks')
    week_number = models.IntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=50, default='Upcoming') # e.g., 'Complete', 'In Progress', 'Upcoming'

    class Meta:
        ordering = ['week_number']

    def __str__(self):
        return f"Week {self.week_number} - {self.title}"
