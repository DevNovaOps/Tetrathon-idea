from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer, NotificationPreferenceSerializer, NotificationHistorySerializer
from .services.notification_service import NotificationService
from .services.preference_service import PreferenceService
from .services.history_service import HistoryService
from .services.summary_service import SummaryService
from .services.filter_service import FilterService

@api_view(['GET'])
@permission_classes([AllowAny])
def list_notifications(request):
    user = request.user if request.user.is_authenticated else None
    if user:
        NotificationService.seed_default_notifications(user)
    qs = Notification.objects.filter(user=user) if user else Notification.objects.none()
    
    # Check if filter or search query param provided
    filter_param = request.GET.get('filter') or request.GET.get('category')
    search_q = request.GET.get('q') or request.GET.get('search')
    if filter_param or search_q:
        qs = FilterService.filter_notifications(user, filter_param=filter_param or 'all', search_query=search_q)
        
    return Response({"notifications": NotificationSerializer(qs, many=True).data})

@api_view(['GET'])
@permission_classes([AllowAny])
def unread_notifications(request):
    user = request.user if request.user.is_authenticated else None
    qs = NotificationService.get_unread(user)
    return Response({
        "count": qs.count(),
        "notifications": NotificationSerializer(qs, many=True).data
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def notification_stats(request):
    user = request.user if request.user.is_authenticated else None
    if user:
        NotificationService.seed_default_notifications(user)
    stats = SummaryService.get_statistics(user)
    return Response(stats)

@api_view(['GET', 'PATCH', 'POST', 'PUT'])
@permission_classes([AllowAny])
def preferences(request):
    user = request.user if request.user.is_authenticated else None
    if not user:
        return Response({"error": "Authentication required"}, status=401)
    
    if request.method in ['PATCH', 'POST', 'PUT']:
        pref = PreferenceService.update_preferences(user, request.data)
        if isinstance(pref, dict) and "error" in pref:
            return Response(pref, status=400)
    else:
        pref = PreferenceService.get_preferences(user)
        
    return Response(NotificationPreferenceSerializer(pref).data)

@api_view(['PATCH', 'POST'])
@permission_classes([AllowAny])
def mark_read(request, id):
    user = request.user if request.user.is_authenticated else None
    notif = NotificationService.mark_as_read(user, id)
    if not notif:
        return Response({"error": "Notification not found"}, status=404)
    return Response({"status": "read", "notification": NotificationSerializer(notif).data})

@api_view(['PATCH', 'POST'])
@permission_classes([AllowAny])
def mark_all_read(request):
    user = request.user if request.user.is_authenticated else None
    count = NotificationService.mark_all_as_read(user)
    return Response({"status": "success", "count": count})

@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_notification(request, id):
    user = request.user if request.user.is_authenticated else None
    success = NotificationService.delete_notification(user, id)
    if not success:
        return Response({"error": "Notification not found"}, status=404)
    return Response({"status": "deleted"})

@api_view(['GET'])
@permission_classes([AllowAny])
def notification_history(request):
    user = request.user if request.user.is_authenticated else None
    export_fmt = request.GET.get('export') or request.GET.get('format')
    
    if export_fmt in ['csv', 'download', 'pdf']:
        csv_data = HistoryService.export_history_data(user)
        response = HttpResponse(csv_data, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="finora_notification_history.csv"'
        return response
        
    qs = HistoryService.get_user_history(user, filter_params=request.GET)
    return Response({"history": NotificationHistorySerializer(qs, many=True).data})

@api_view(['GET'])
@permission_classes([AllowAny])
def filter_notifications_view(request):
    user = request.user if request.user.is_authenticated else None
    if user:
        NotificationService.seed_default_notifications(user)
    filter_param = request.GET.get('filter') or request.GET.get('category') or 'all'
    search_q = request.GET.get('q') or request.GET.get('search')
    qs = FilterService.filter_notifications(user, filter_param=filter_param, search_query=search_q)
    return Response({"notifications": NotificationSerializer(qs, many=True).data})

@api_view(['GET'])
@permission_classes([AllowAny])
def search_notifications_view(request):
    user = request.user if request.user.is_authenticated else None
    if user:
        NotificationService.seed_default_notifications(user)
    search_q = request.GET.get('q') or request.GET.get('query') or ''
    qs = FilterService.filter_notifications(user, filter_param='all', search_query=search_q)
    return Response({"notifications": NotificationSerializer(qs, many=True).data})
