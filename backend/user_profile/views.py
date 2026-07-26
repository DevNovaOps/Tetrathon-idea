from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from .services.profile_service import ProfileService
from .services.snapshot_service import SnapshotService
from .services.goal_service import GoalService
from .services.connected_services_service import ConnectedServicesService
from .services.timeline_service import TimelineService
from .services.explainability_service import ExplainabilityService
from .services.export_service import ExportService
from .serializers import (
    UserProfileSerializer, FinancialGoalSerializer, ConnectedBankSerializer,
    ConnectedUPISerializer, ConnectedCardSerializer, UserTimelineSerializer
)

@api_view(['GET'])
@permission_classes([AllowAny])
def profile_overview(request):
    user = request.user if request.user.is_authenticated else None
    if user:
        GoalService.seed_default_goals(user)
        ConnectedServicesService.seed_default_services(user)
        TimelineService.seed_default_timeline(user)
        
    profile = ProfileService.get_profile(user)
    snapshot = SnapshotService.get_financial_snapshot(user)
    goals = GoalService.get_goals(user)
    services = ConnectedServicesService.get_services(user)
    timeline = TimelineService.get_timeline(user, limit=15)
    explainability = ExplainabilityService.get_latest_summary(user)
    stats = ExplainabilityService.get_account_statistics(user)
    about_me = ExplainabilityService.get_about_me(user)

    return Response({
        "profile": UserProfileSerializer(profile).data if profile else {},
        "financial_snapshot": snapshot,
        "goals": FinancialGoalSerializer(goals, many=True).data,
        "connected_services": {
            "banks": ConnectedBankSerializer(services["banks"], many=True).data,
            "upis": ConnectedUPISerializer(services["upis"], many=True).data,
            "cards": ConnectedCardSerializer(services["cards"], many=True).data,
        },
        "timeline_events": UserTimelineSerializer(timeline, many=True).data,
        "explainable_ai": explainability,
        "account_statistics": stats,
        "about_me": about_me
    })

@api_view(['PATCH', 'POST', 'PUT'])
@permission_classes([AllowAny])
def update_profile_view(request):
    user = request.user if request.user.is_authenticated else None
    if not user:
        return Response({"error": "Authentication required"}, status=401)
    res = ProfileService.update_profile(user, request.data)
    if isinstance(res, dict) and "error" in res:
        return Response(res, status=400)
    return Response(UserProfileSerializer(res).data)

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def goals_list_create(request):
    user = request.user if request.user.is_authenticated else None
    if request.method == 'POST':
        res = GoalService.create_goal(user, request.data)
        if isinstance(res, dict) and "error" in res:
            return Response(res, status=400)
        return Response(FinancialGoalSerializer(res).data, status=201)
    
    if user:
        GoalService.seed_default_goals(user)
    goals = GoalService.get_goals(user)
    return Response({"goals": FinancialGoalSerializer(goals, many=True).data})

@api_view(['PATCH', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def goal_detail(request, id):
    user = request.user if request.user.is_authenticated else None
    if request.method == 'DELETE':
        success = GoalService.delete_goal(user, id)
        if not success:
            return Response({"error": "Goal not found"}, status=404)
        return Response({"status": "deleted"})
        
    res = GoalService.update_goal(user, id, request.data)
    if isinstance(res, dict) and "error" in res:
        return Response(res, status=400)
    return Response(FinancialGoalSerializer(res).data)

@api_view(['POST'])
@permission_classes([AllowAny])
def goal_contribute(request, id):
    user = request.user if request.user.is_authenticated else None
    amt = request.data.get('amount')
    if not amt:
        return Response({"error": "Amount is required"}, status=400)
    res = GoalService.add_contribution(user, id, amt, request.data.get('notes', ''))
    if isinstance(res, dict) and "error" in res:
        return Response(res, status=400)
    return Response(FinancialGoalSerializer(res).data)

@api_view(['POST', 'PATCH'])
@permission_classes([AllowAny])
def set_active_goal_view(request, id):
    user = request.user if request.user.is_authenticated else None
    res = GoalService.set_active_primary_goal(user, id)
    if not res:
        return Response({"error": "Goal not found"}, status=404)
    return Response(FinancialGoalSerializer(res).data)

@api_view(['GET'])
@permission_classes([AllowAny])
def connected_services_view(request):
    user = request.user if request.user.is_authenticated else None
    if user:
        ConnectedServicesService.seed_default_services(user)
    services = ConnectedServicesService.get_services(user)
    return Response({
        "banks": ConnectedBankSerializer(services["banks"], many=True).data,
        "upis": ConnectedUPISerializer(services["upis"], many=True).data,
        "cards": ConnectedCardSerializer(services["cards"], many=True).data,
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def add_service_view(request, service_type):
    user = request.user if request.user.is_authenticated else None
    st = service_type.lower()
    if st == 'bank':
        res = ConnectedServicesService.add_bank(user, request.data)
        return Response(ConnectedBankSerializer(res).data, status=201)
    elif st == 'upi':
        res = ConnectedServicesService.add_upi(user, request.data)
        return Response(ConnectedUPISerializer(res).data, status=201)
    elif st == 'card':
        res = ConnectedServicesService.add_card(user, request.data)
        return Response(ConnectedCardSerializer(res).data, status=201)
    return Response({"error": "Invalid service type"}, status=400)

@api_view(['DELETE'])
@permission_classes([AllowAny])
def remove_service_view(request, service_type, id):
    user = request.user if request.user.is_authenticated else None
    success = ConnectedServicesService.remove_service(user, service_type, id)
    if not success:
        return Response({"error": "Service not found"}, status=404)
    return Response({"status": "deleted"})

@api_view(['GET'])
@permission_classes([AllowAny])
def timeline_view(request):
    user = request.user if request.user.is_authenticated else None
    if user:
        TimelineService.seed_default_timeline(user)
    limit = int(request.GET.get('limit', 50))
    events = TimelineService.get_timeline(user, limit=limit)
    return Response({"timeline": UserTimelineSerializer(events, many=True).data})

@api_view(['GET'])
@permission_classes([AllowAny])
def explainability_view(request):
    user = request.user if request.user.is_authenticated else None
    summary = ExplainabilityService.get_latest_summary(user)
    about = ExplainabilityService.get_about_me(user)
    stats = ExplainabilityService.get_account_statistics(user)
    return Response({
        "explainable_ai": summary,
        "about_me": about,
        "account_statistics": stats
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def export_data_view(request):
    user = request.user if request.user.is_authenticated else None
    fmt = request.GET.get('format', 'json')
    return ExportService.export_data_response(user, format_type=fmt)
