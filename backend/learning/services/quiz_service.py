from learning.models import Quiz
from learning.services.lesson_service import LessonService
from achievements.services.reward_service import RewardService

class QuizService:
    @staticmethod
    def evaluate_submission(user, quiz_id, selected_option):
        quiz = Quiz.objects.select_related("lesson", "lesson__course").filter(lesson__id=quiz_id).first()
        if not quiz:
            try:
                quiz = Quiz.objects.select_related("lesson", "lesson__course").get(id=quiz_id)
            except (Quiz.DoesNotExist, ValueError):
                return {"error": "Quiz not found"}

        try:
            selected_idx = int(selected_option)
        except (ValueError, TypeError):
            selected_idx = -1

        is_correct = (selected_idx == quiz.correct_answer)
        lesson = quiz.lesson

        if is_correct:
            # Award quiz XP
            if user and user.is_authenticated:
                RewardService.award_xp(user, quiz.marks, reason=f"Passed Quiz: {lesson.title}")
            
            # Complete lesson
            completion_res = LessonService.complete_lesson(user, lesson.id)
            
            # Find next lesson
            all_lessons = list(lesson.course.lessons.all())
            next_id = ""
            for idx, l in enumerate(all_lessons):
                if l.id == lesson.id and idx < len(all_lessons) - 1:
                    next_id = str(all_lessons[idx+1].id)
                    break

            return {
                "passed": True,
                "score": f"{quiz.marks}/{quiz.marks}",
                "percentage": 100,
                "explanation": f"Correct! {quiz.explanation}",
                "xp_awarded": quiz.marks + (completion_res.get("xp_awarded", 0) if isinstance(completion_res, dict) else 0),
                "next_lesson_id": next_id,
                "unlocked": completion_res.get("unlocked", []) if isinstance(completion_res, dict) else []
            }
        else:
            return {
                "passed": False,
                "score": f"0/{quiz.marks}",
                "percentage": 0,
                "explanation": f"Not quite. {quiz.explanation} Try again to unlock the next lesson!",
                "retry": True
            }
