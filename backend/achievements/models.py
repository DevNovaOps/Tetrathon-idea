import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone

class Badge(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=150)
    description = models.TextField()
    icon = models.CharField(max_length=50, default="🏆")
    xp = models.IntegerField(default=20)
    unlock_rule = models.CharField(max_length=100, unique=True)
    target_value = models.FloatField(default=1.0)
    is_milestone = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.icon} {self.title} ({self.xp} XP)"

class Achievement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="achievements")
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name="user_achievements")
    unlocked = models.BooleanField(default=False)
    unlocked_at = models.DateTimeField(null=True, blank=True)
    progress = models.FloatField(default=0.0)
    required_progress = models.FloatField(default=1.0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "badge")

    def __str__(self):
        status = "Unlocked" if self.unlocked else f"{self.progress}/{self.required_progress}"
        return f"{self.user} - {self.badge.title} ({status})"

class UserLevel(models.Model):
    LEVEL_THRESHOLDS = [
        (0, "Beginner"),
        (100, "Intermediate"),
        (300, "Advanced"),
        (600, "Expert"),
        (1000, "Finance Explorer"),
        (1500, "Finance Master"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="level_stats")
    xp = models.IntegerField(default=0)
    current_level = models.CharField(max_length=50, default="Beginner")
    longest_streak = models.IntegerField(default=0)
    current_streak = models.IntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True)

    def update_level(self):
        new_level = "Beginner"
        for threshold, name in sorted(self.LEVEL_THRESHOLDS):
            if self.xp >= threshold:
                new_level = name
        if self.current_level != new_level:
            self.current_level = new_level
            return True
        return False

    def __str__(self):
        return f"{self.user} - {self.current_level} ({self.xp} XP)"
