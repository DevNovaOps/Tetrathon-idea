from learning.models import Lesson, Course, UserProgress, Quiz
from learning.services.streak_service import StreakService
from achievements.services.reward_service import RewardService
from achievements.services.unlock_service import UnlockService
from django.utils import timezone

class LessonService:
    @staticmethod
    def get_lesson_detail(user, lesson_id):
        try:
            lesson = Lesson.objects.select_related("course").get(id=lesson_id)
        except Lesson.DoesNotExist:
            return None

        course = lesson.course
        all_lessons = list(course.lessons.all())
        prev_id = ""
        next_id = ""
        for idx, l in enumerate(all_lessons):
            if l.id == lesson.id:
                if idx > 0:
                    prev_id = str(all_lessons[idx-1].id)
                if idx < len(all_lessons) - 1:
                    next_id = str(all_lessons[idx+1].id)
                break

        completed = False
        if user and user.is_authenticated:
            completed = UserProgress.objects.filter(user=user, lesson=lesson, completed=True).exists()

        quiz = lesson.quizzes.first()
        quiz_data = None
        if quiz:
            quiz_data = {
                "id": str(quiz.id),
                "question": quiz.question,
                "options": quiz.options,
                "marks": quiz.marks
            }

        return {
            "id": str(lesson.id),
            "course_id": str(course.id),
            "course_title": course.title,
            "title": lesson.title,
            "order": lesson.order,
            "duration": f"{lesson.duration} min read",
            "content": lesson.content,
            "article": lesson.article or lesson.content,
            "video_url": lesson.video_url or "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "xp_reward": lesson.xp_reward,
            "completed": completed,
            "prev_lesson_id": prev_id,
            "next_lesson_id": next_id,
            "quiz": quiz_data
        }

    @staticmethod
    def complete_lesson(user, lesson_id):
        try:
            lesson = Lesson.objects.select_related("course").get(id=lesson_id)
        except Lesson.DoesNotExist:
            return {"error": "Lesson not found"}

        if not user or not user.is_authenticated:
            return {"status": "completed", "xp_awarded": lesson.xp_reward, "new_xp": 120, "level": "Intermediate", "unlocked": []}

        up, created = UserProgress.objects.get_or_create(
            user=user, course=lesson.course, lesson=lesson,
            defaults={"completed": True, "completion_pct": 100.0, "completed_at": timezone.now()}
        )
        
        xp_res = None
        unlocked = []
        if created or not up.completed:
            up.completed = True
            up.completion_pct = 100.0
            up.completed_at = timezone.now()
            up.save()

            # Award XP
            xp_res = RewardService.award_xp(user, lesson.xp_reward, reason=f"Completed lesson: {lesson.title}")

            # Update streak
            StreakService.update_streak(user)

            # Trigger achievement events
            unlocked = UnlockService.check_and_unlock(user, "lesson_completed", 1)

            # Check if course is now fully completed
            total_l = lesson.course.lessons.count()
            user_l = UserProgress.objects.filter(user=user, course=lesson.course, completed=True).count()
            if user_l >= total_l and total_l > 0:
                RewardService.award_xp(user, 100, reason=f"Completed course: {lesson.course.title}")
                course_unlocked = UnlockService.check_and_unlock(user, "course_completed", 1)
                unlocked.extend(course_unlocked)
        else:
            up.last_accessed = timezone.now()
            up.save()

        level_info = RewardService.get_user_level(user)
        return {
            "status": "completed",
            "xp_awarded": lesson.xp_reward if (created or xp_res) else 0,
            "new_xp": level_info["xp"],
            "level": level_info["current_level"],
            "unlocked": unlocked
        }
