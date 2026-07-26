from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .services.settings_service import SettingsService
from .serializers import UserPreferenceSerializer
from notifications.serializers import NotificationPreferenceSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def settings_overview(request):
    user = request.user if request.user.is_authenticated else None
    pref = SettingsService.get_preferences(user)
    notif_pref = SettingsService.get_notification_preferences(user)
    
    return Response({
        "appearance": UserPreferenceSerializer(pref).data if pref else {},
        "notifications": NotificationPreferenceSerializer(notif_pref).data if notif_pref else {},
        "user": {
            "email": user.email if user else "",
            "full_name": user.full_name if user else "",
            "timezone": user.timezone if user else "UTC",
            "currency": user.preferred_currency if user else "INR"
        }
    })

@api_view(['PATCH', 'POST', 'PUT'])
@permission_classes([AllowAny])
def update_settings_view(request):
    user = request.user if request.user.is_authenticated else None
    if not user:
        return Response({"error": "Authentication required"}, status=401)
    res = SettingsService.update_preferences(user, request.data)
    if isinstance(res, dict) and "error" in res:
        return Response(res, status=400)
    return Response(UserPreferenceSerializer(res).data)

@api_view(['GET', 'PATCH', 'POST', 'PUT'])
@permission_classes([AllowAny])
def settings_notifications_view(request):
    user = request.user if request.user.is_authenticated else None
    if not user:
        return Response({"error": "Authentication required"}, status=401)
    if request.method in ['PATCH', 'POST', 'PUT']:
        res = SettingsService.update_notification_preferences(user, request.data)
        if isinstance(res, dict) and "error" in res:
            return Response(res, status=400)
        return Response(NotificationPreferenceSerializer(res).data)
    
    pref = SettingsService.get_notification_preferences(user)
    return Response(NotificationPreferenceSerializer(pref).data)

@api_view(['POST'])
@permission_classes([AllowAny])
def privacy_action_view(request):
    user = request.user if request.user.is_authenticated else None
    if not user:
        return Response({"error": "Authentication required"}, status=401)
    
    action = request.data.get('action')
    if action == 'logout_all_devices':
        # Log out all sessions
        from django.contrib.sessions.models import Session
        Session.objects.all().delete()
        return Response({"status": "success", "message": "Logged out from all active sessions."})
    elif action == 'delete_account':
        # Soft deactivate user
        user.is_active = False
        user.save()
        return Response({"status": "success", "message": "Account deactivated."})
    elif action == 'toggle_2fa':
        pref = SettingsService.get_preferences(user)
        pref.two_factor_ready = not pref.two_factor_ready
        pref.save()
        return Response({"status": "success", "two_factor_ready": pref.two_factor_ready})
    return Response({"error": "Unknown privacy action"}, status=400)
