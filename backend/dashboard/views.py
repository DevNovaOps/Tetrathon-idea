"""Dashboard API Views."""
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import DashboardAnalyticsService


class DashboardAPIView(APIView):
    """
    GET /api/dashboard/
    Aggregate all dashboard data in a single request.
    """
    
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        try:
            # Note: We rely on the related_name 'profile' set in models.py
            profile = getattr(request.user, 'profile', None)
            
            if not profile:
                return Response(
                    {"success": False, "message": "User profile not found. Complete onboarding."},
                    status=status.HTTP_404_NOT_FOUND
                )

            service = DashboardAnalyticsService(request.user, profile)
            data = service.get_dashboard_data()

            return Response(
                {"success": True, "data": data},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            import logging
            logger = logging.getLogger('dashboard')
            logger.exception("Failed to fetch dashboard data")
            
            return Response(
                {"success": False, "message": "An error occurred fetching dashboard data."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
