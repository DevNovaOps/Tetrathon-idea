from learning.models import LearningStreak
from achievements.services.unlock_service import UnlockService
from django.utils import timezone
import datetime

class StreakService:
    @staticmethod
    def update_streak(user):
        if not user or not user.is_authenticated:
            return None
        
        streak_obj, _ = LearningStreak.objects.get_or_create(user=user)
        today = timezone.now().date()
        
        if streak_obj.last_learning_date == today:
            # Already logged learning today
            return streak_obj
        
        yesterday = today - datetime.timedelta(days=1)
        if streak_obj.last_learning_date == yesterday:
            streak_obj.current_streak += 1
        else:
            streak_obj.current_streak = 1
            
        if streak_obj.current_streak > streak_obj.longest_streak:
            streak_obj.longest_streak = streak_obj.current_streak
            
        streak_obj.last_learning_date = today
        streak_obj.save()

        # Update UserLevel streak as well
        try:
            from achievements.models import UserLevel
            level_obj, _ = UserLevel.objects.get_or_create(user=user)
            level_obj.current_streak = streak_obj.current_streak
            level_obj.longest_streak = streak_obj.longest_streak
            level_obj.last_activity_date = today
            level_obj.save()
        except Exception:
            pass

        # Trigger streak achievements!
        UnlockService.check_and_unlock(user, "streak_updated", streak_obj.current_streak)
        return streak_obj

    @staticmethod
    def get_streak(user):
        if not user or not user.is_authenticated:
            return {"current": 14, "longest": 21}
        streak_obj, _ = LearningStreak.objects.get_or_create(user=user)
        return {"current": streak_obj.current_streak, "longest": streak_obj.longest_streak}
