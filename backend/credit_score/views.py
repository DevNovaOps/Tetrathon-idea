"""
Views for the Credit Score Module.
Thin controllers that delegate business logic to the Service Layer.
"""
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .services import CreditScoreService

logger = logging.getLogger('credit_score')

class CreditScoreAPIView(APIView):
    """
    GET /api/credit-score/
    Returns the fully calculated, deterministic credit score response.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            data = CreditScoreService.get_or_calculate_credit_profile(request.user)
            return Response({
                "success": True,
                "data": data
            }, status=status.HTTP_200_OK)
            
        except ValueError as e:
            logger.warning(f"Credit Score API Error: {str(e)} for user {request.user.email}")
            return Response({
                "success": False,
                "message": str(e)
            }, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            logger.exception(f"Unexpected error in CreditScoreAPIView: {str(e)}")
            return Response({
                "success": False,
                "message": "An internal error occurred while calculating the credit score."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
