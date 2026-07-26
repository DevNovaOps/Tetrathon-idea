from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .services import DigitalSignalService


@api_view(['GET', 'PATCH', 'PUT'])
@permission_classes([IsAuthenticated])
def digital_signals_view(request):
    """
    GET  — Retrieve signals + derived features.
    PATCH/PUT — Update signals → cascade to credit score + risk profile.
    """
    if request.method == 'GET':
        data = DigitalSignalService.get_full_profile(request.user)
        return Response(data)

    data = DigitalSignalService.update_signals(request.user, request.data)
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def derived_features_view(request):
    """Returns only the 5 derived feature scores."""
    profile = DigitalSignalService.get_or_create(request.user)
    from .feature_engine import DigitalFeatureEngine
    features = DigitalFeatureEngine(profile).calculate_all()
    return Response({"derived_features": features})
