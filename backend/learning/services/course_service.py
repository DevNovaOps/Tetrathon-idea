from learning.models import Course, Lesson, UserProgress
from learning.services.progress_service import ProgressService

class CourseService:
    @staticmethod
    def get_categories_grid(user):
        # The 9 categories matching reference image 13
        category_defs = [
            {"name": "What is Credit Score?", "icon": "🛡️", "bg": "purple-bg", "desc": "Understand how credit score works."},
            {"name": "Mutual Funds", "icon": "📊", "bg": "green-bg", "desc": "Learn about mutual funds and types."},
            {"name": "SIPs", "icon": "💰", "bg": "blue-bg", "desc": "Everything about Systematic Investment Plans."},
            {"name": "Emergency Fund", "icon": "🛟", "bg": "cyan-bg", "desc": "Why it's important and how to build one."},
            {"name": "Financial Literacy", "icon": "📖", "bg": "orange-bg", "desc": "Basic financial concepts everyone should know."},
            {"name": "Budgeting", "icon": "💳", "bg": "red-bg", "desc": "How to budget and manage money."},
            {"name": "Stock Market Basics", "icon": "📈", "bg": "emerald-bg", "desc": "Introduction to equities and trading."},
            {"name": "Tax Planning", "icon": "🏛️", "bg": "pink-bg", "desc": "Save more through smart tax strategies."},
            {"name": "Financial Security", "icon": "🔐", "bg": "blue-bg", "desc": "Protect your wealth and identity."},
        ]

        result = []
        for cat in category_defs:
            course = Course.objects.filter(category=cat["name"]).first()
            if course:
                lesson_count = course.lessons.count()
                course_id = str(course.id)
                progress = ProgressService.get_course_progress(user, course)
            else:
                lesson_count = 4
                course_id = ""
                progress = 0

            result.append({
                "id": course_id,
                "name": cat["name"],
                "icon": cat["icon"],
                "bg_class": cat["bg"],
                "description": cat["desc"],
                "lesson_count_text": f"{lesson_count} Lessons",
                "progress_pct": progress
            })
        return result

    @staticmethod
    def get_featured_course_data(user):
        course = Course.objects.filter(category="Featured Course").first()
        if not course:
            course = Course.objects.first()

        if not course:
            return {
                "id": "",
                "title": "Master Personal Finance",
                "description": "A comprehensive beginner-friendly course covering budgeting, saving, investing, and building long-term financial security.",
                "hours_text": "⏱ 4 Hours",
                "lessons_text": "📚 12 Lessons",
                "difficulty_text": "🟢 Beginner",
                "progress_pct": 65,
                "next_lesson_id": ""
            }

        progress = ProgressService.get_course_progress(user, course)
        next_lesson_id = ""
        first_lesson = course.lessons.first()
        if first_lesson:
            next_lesson_id = str(first_lesson.id)
            if user and user.is_authenticated:
                for l in course.lessons.all():
                    up = UserProgress.objects.filter(user=user, lesson=l, completed=True).exists()
                    if not up:
                        next_lesson_id = str(l.id)
                        break

        return {
            "id": str(course.id),
            "title": course.title,
            "description": course.description,
            "hours_text": f"⏱ {int(course.estimated_hours)} Hours" if course.estimated_hours.is_integer() else f"⏱ {course.estimated_hours} Hours",
            "lessons_text": f"📚 {course.lessons.count()} Lessons",
            "difficulty_text": f"🟢 {course.difficulty}",
            "progress_pct": progress,
            "next_lesson_id": next_lesson_id
        }

    @staticmethod
    def get_course_detail_data(user, course_id):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return None

        lessons = []
        for idx, l in enumerate(course.lessons.all(), 1):
            completed = False
            if user and user.is_authenticated:
                completed = UserProgress.objects.filter(user=user, lesson=l, completed=True).exists()
            lessons.append({
                "id": str(l.id),
                "order": idx,
                "title": l.title,
                "duration": f"{l.duration} mins",
                "xp": l.xp_reward,
                "completed": completed
            })

        return {
            "id": str(course.id),
            "title": course.title,
            "category": course.category,
            "description": course.description,
            "difficulty": course.difficulty,
            "hours": course.estimated_hours,
            "total_lessons": len(lessons),
            "progress_pct": ProgressService.get_course_progress(user, course),
            "lessons": lessons
        }
