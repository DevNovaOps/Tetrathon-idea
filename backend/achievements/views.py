from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from achievements.services.achievement_service import AchievementService
from achievements.services.statistics_service import StatisticsService
from achievements.services.badge_service import BadgeService
from achievements.services.unlock_service import UnlockService
from achievements.models import Achievement, Badge

@api_view(['GET'])
@permission_classes([AllowAny])
def achievements_summary(request):
    user = request.user if request.user.is_authenticated else None
    if user:
        UnlockService.sync_course_badges(user)
    summary = AchievementService.get_summary_data(user)
    unlocked = AchievementService.get_unlocked_grid(user)
    locked = AchievementService.get_locked_milestones(user)
    stats = StatisticsService.get_user_statistics(user)

    return Response({
        "summary": summary,
        "unlocked_achievements": unlocked,
        "locked_milestones": locked,
        "statistics": stats
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def statistics(request):
    user = request.user if request.user.is_authenticated else None
    stats = StatisticsService.get_user_statistics(user)
    return Response({"statistics": stats})

@api_view(['GET'])
@permission_classes([AllowAny])
def progress(request):
    user = request.user if request.user.is_authenticated else None
    summary = AchievementService.get_summary_data(user)
    locked = AchievementService.get_locked_milestones(user)
    return Response({
        "summary": summary,
        "progress_items": locked
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def badges(request):
    BadgeService.seed_default_badges()
    all_badges = BadgeService.get_all_badges()
    res = [
        {
            "id": str(b.id),
            "title": b.title,
            "description": b.description,
            "icon": b.icon,
            "xp": b.xp,
            "is_milestone": b.is_milestone
        }
        for b in all_badges
    ]
    return Response({"badges": res})

@api_view(['GET'])
@permission_classes([AllowAny])
def history(request):
    user = request.user if request.user.is_authenticated else None
    unlocked = AchievementService.get_unlocked_grid(user)
    return Response({"history": unlocked})

@api_view(['GET'])
@permission_classes([AllowAny])
def explain_achievement(request, id):
    user = request.user if request.user.is_authenticated else None
    insight = AchievementService.get_explainable_ai_insight(user, id)
    return Response(insight)
