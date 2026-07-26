from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from notifications.services.event_service import EventService

try:
    from learning.models import UserProgress
    @receiver(post_save, sender=UserProgress)
    def handle_lesson_completed_signal(sender, instance, created, **kwargs):
        if instance.completed and instance.user:
            # Check if this lesson completion was just saved
            lesson_title = instance.lesson.title if instance.lesson else "Lesson"
            xp = instance.lesson.xp_reward if instance.lesson else 50
            EventService.notify_lesson_completed(instance.user, lesson_title, xp)
except ImportError:
    pass

try:
    from achievements.models import Achievement
    @receiver(post_save, sender=Achievement)
    def handle_badge_unlocked_signal(sender, instance, created, **kwargs):
        if instance.unlocked and instance.user:
            EventService.notify_badge_unlocked(instance.user, instance.title, instance.xp)
except ImportError:
    pass
