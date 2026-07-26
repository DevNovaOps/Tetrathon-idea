from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from learning.services.content_service import ContentService
from learning.services.progress_service import ProgressService
from learning.services.course_service import CourseService
from learning.services.lesson_service import LessonService
from learning.services.recommendation_service import RecommendationService
from learning.services.quiz_service import QuizService
from achievements.services.achievement_service import AchievementService
from learning.models import Course, Lesson

@api_view(['GET'])
@permission_classes([AllowAny])
def dashboard(request):
    ContentService.seed_all_content()
    user = request.user if request.user.is_authenticated else None

    progress = ProgressService.get_dashboard_progress(user)
    featured = CourseService.get_featured_course_data(user)
    categories = CourseService.get_categories_grid(user)
    articles = RecommendationService.get_recommended_articles(user)
    tips = RecommendationService.get_ai_learning_tips(user)
    unlocked_badges = AchievementService.get_unlocked_grid(user)[:8]

    return Response({
        "progress": progress,
        "featured_course": featured,
        "categories": categories,
        "articles": articles,
        "tips": tips,
        "badges_preview": unlocked_badges
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def courses(request):
    ContentService.seed_all_content()
    user = request.user if request.user.is_authenticated else None
    cat_filter = request.GET.get('category')

    query = Course.objects.all()
    if cat_filter:
        query = query.filter(category__icontains=cat_filter)

    res = []
    for c in query:
        res.append({
            "id": str(c.id),
            "title": c.title,
            "category": c.category,
            "difficulty": c.difficulty,
            "hours": c.estimated_hours,
            "total_lessons": c.total_lessons,
            "thumbnail": c.thumbnail,
            "progress_pct": ProgressService.get_course_progress(user, c)
        })
    return Response({"courses": res})

@api_view(['GET'])
@permission_classes([AllowAny])
def course_detail(request, id):
    ContentService.seed_all_content()
    user = request.user if request.user.is_authenticated else None
    data = CourseService.get_course_detail_data(user, id)
    if not data:
        return Response({"error": "Course not found"}, status=404)
    return Response(data)

@api_view(['GET'])
@permission_classes([AllowAny])
def lesson_detail(request, id):
    ContentService.seed_all_content()
    user = request.user if request.user.is_authenticated else None
    data = LessonService.get_lesson_detail(user, id)
    if not data:
        return Response({"error": "Lesson not found"}, status=404)
    return Response(data)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def complete_lesson(request, id):
    user = request.user if request.user.is_authenticated else None
    res = LessonService.complete_lesson(user, id)
    if "error" in res:
        return Response(res, status=400)
    return Response(res)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def submit_quiz(request, id):
    user = request.user if request.user.is_authenticated else None
    selected_option = request.data.get('selected_option', request.data.get('option', 0))
    res = QuizService.evaluate_submission(user, id, selected_option)
    if "error" in res:
        return Response(res, status=400)
    return Response(res)

@api_view(['GET'])
@permission_classes([AllowAny])
def recommendations(request):
    ContentService.seed_all_content()
    user = request.user if request.user.is_authenticated else None
    recs = RecommendationService.get_recommendations(user)
    return Response({"recommendations": recs})

@api_view(['GET'])
@permission_classes([AllowAny])
def progress(request):
    user = request.user if request.user.is_authenticated else None
    prog = ProgressService.get_dashboard_progress(user)
    return Response({"progress": prog})
