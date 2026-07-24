"""Onboarding API views."""
import logging

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserProfile
from .serializers import ReviewSerializer, Step1Serializer, Step2Serializer, Step3Serializer
from .services import finish_onboarding, save_step1, save_step2, save_step3

logger = logging.getLogger('onboarding')


class Step1View(APIView):
    """POST /api/onboarding/step1/ — save personal information."""

    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        serializer = Step1Serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'success': False, 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            profile = save_step1(request.user, serializer.validated_data)
            return Response(
                {
                    'success': True,
                    'message': 'Personal information saved successfully.',
                    'data': {
                        'current_step': profile.current_step,
                        'step1_completed': profile.step1_completed,
                    },
                },
                status=status.HTTP_200_OK,
            )
        except Exception:
            logger.exception('Step 1 save failed for %s', request.user.email)
            return Response(
                {'success': False, 'message': 'Something went wrong.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class Step2View(APIView):
    """POST /api/onboarding/step2/ — save financial profile."""

    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        serializer = Step2Serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'success': False, 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            profile = save_step2(request.user, serializer.validated_data)
            return Response(
                {
                    'success': True,
                    'message': 'Financial profile saved successfully.',
                    'data': {
                        'current_step': profile.current_step,
                        'step2_completed': profile.step2_completed,
                    },
                },
                status=status.HTTP_200_OK,
            )
        except Exception:
            logger.exception('Step 2 save failed for %s', request.user.email)
            return Response(
                {'success': False, 'message': 'Something went wrong.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class Step3View(APIView):
    """POST /api/onboarding/step3/ — save investment profile."""

    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        serializer = Step3Serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'success': False, 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            profile = save_step3(request.user, serializer.validated_data)
            return Response(
                {
                    'success': True,
                    'message': 'Investment profile saved successfully.',
                    'data': {
                        'current_step': profile.current_step,
                        'step3_completed': profile.step3_completed,
                    },
                },
                status=status.HTTP_200_OK,
            )
        except Exception:
            logger.exception('Step 3 save failed for %s', request.user.email)
            return Response(
                {'success': False, 'message': 'Something went wrong.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ReviewView(APIView):
    """GET /api/onboarding/review/ — return all onboarding data for summary."""

    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        try:
            profile, _ = UserProfile.objects.select_related('user').get_or_create(
                user=request.user,
            )
            return Response(
                {
                    'success': True,
                    'data': ReviewSerializer(profile).data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception:
            logger.exception('Review fetch failed for %s', request.user.email)
            return Response(
                {'success': False, 'message': 'Something went wrong.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class FinishView(APIView):
    """POST /api/onboarding/finish/ — mark onboarding complete."""

    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        try:
            profile = finish_onboarding(request.user)
            return Response(
                {
                    'success': True,
                    'message': 'Onboarding completed successfully! Welcome to Finora.',
                    'data': {
                        'onboarding_completed': profile.onboarding_completed,
                        'redirect': '/04-dashboard/dashboard.html',
                    },
                },
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response(
                {'success': False, 'message': str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception:
            logger.exception('Finish onboarding failed for %s', request.user.email)
            return Response(
                {'success': False, 'message': 'Something went wrong.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
