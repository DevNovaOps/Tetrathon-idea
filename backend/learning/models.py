import uuid
from django.db import models
from django.conf import settings

class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.CharField(max_length=50, default="Beginner")
    category = models.CharField(max_length=100)
    thumbnail = models.CharField(max_length=50, default="📘")
    estimated_hours = models.FloatField(default=1.0)
    total_lessons = models.IntegerField(default=0)
    status = models.CharField(max_length=50, default="Active")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.category})"

class Lesson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=200)
    content = models.TextField()
    video_url = models.CharField(max_length=500, null=True, blank=True)
    article = models.TextField(null=True, blank=True)
    duration = models.IntegerField(default=15)
    order = models.IntegerField(default=1)
    xp_reward = models.IntegerField(default=20)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.course.title} - {self.order}. {self.title}"

class Quiz(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="quizzes")
    question = models.TextField()
    options = models.JSONField(default=list)
    correct_answer = models.IntegerField(default=0)
    explanation = models.TextField()
    marks = models.IntegerField(default=30)

    def __str__(self):
        return f"Quiz for {self.lesson.title}"

class UserProgress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="learning_progress")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="user_progress")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="user_progress")
    completed = models.BooleanField(default=False)
    completion_pct = models.FloatField(default=0.0)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "lesson")

    def __str__(self):
        return f"{self.user} - {self.lesson.title} ({'Done' if self.completed else 'In Progress'})"

class LearningStreak(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="learning_streak")
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_learning_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.current_streak} days"

class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    tag = models.CharField(max_length=50)
    tag_color = models.CharField(max_length=50, default="blue-tag")
    summary = models.TextField()
    read_time = models.CharField(max_length=50, default="5 min read")
    difficulty = models.CharField(max_length=50, default="Beginner")
    content = models.TextField()
    url = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title

class AiTip(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="ai_tips")
    title = models.CharField(max_length=200)
    content = models.TextField()
    icon = models.CharField(max_length=50, default="💡")
    icon_bg = models.CharField(max_length=50, default="green-bg")
    category = models.CharField(max_length=100, default="General")
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title
