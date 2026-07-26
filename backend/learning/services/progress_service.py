from learning.models import Course, Lesson, UserProgress
from learning.services.streak_service import StreakService
from achievements.services.reward_service import RewardService
from achievements.services.unlock_service import UnlockService

class ProgressService:
    @staticmethod
    def get_dashboard_progress(user):
        if not user or not user.is_authenticated:
            return {
                "completion_pct": 60,
                "lessons_completed": 18,
                "total_lessons": 30,
                "current_level": "Intermediate",
                "learning_streak": 14,
                "learning_hours": "2.5h"
            }

        UnlockService.sync_course_badges(user)
        total_lessons = Lesson.objects.count()
        if total_lessons == 0:
            return {
                "completion_pct": 0,
                "lessons_completed": 0,
                "total_lessons": 0,
                "current_level": "Beginner",
                "learning_streak": 0,
                "learning_hours": "0h"
            }

        completed_progress = UserProgress.objects.filter(user=user, completed=True)
        lessons_completed = completed_progress.count()
        completion_pct = round((lessons_completed / total_lessons) * 100)
        if completion_pct > 100:
            completion_pct = 100

        # Calculate learning hours
        completed_lesson_ids = completed_progress.values_list("lesson_id", flat=True)
        completed_lessons = Lesson.objects.filter(id__in=completed_lesson_ids)
        total_minutes = sum(l.duration for l in completed_lessons)
        hours = round(total_minutes / 60.0, 1)
        hours_str = f"{int(hours)}h" if hours.is_integer() else f"{hours}h"

        level_info = RewardService.get_user_level(user)
        streak_info = StreakService.get_streak(user)

        return {
            "completion_pct": completion_pct,
            "lessons_completed": lessons_completed,
            "total_lessons": total_lessons,
            "current_level": level_info["current_level"],
            "learning_streak": streak_info["current"],
            "learning_hours": hours_str,
            "xp": level_info["xp"]
        }

    @staticmethod
    def get_course_progress(user, course):
        total_l = course.lessons.count()
        if total_l == 0:
            return 0
        if not user or not user.is_authenticated:
            # Demo values
            if course.category == "Featured Course":
                return 65
            return 0
        completed_l = UserProgress.objects.filter(user=user, course=course, completed=True).count()
        return round((completed_l / total_l) * 100)
