"""Authentication API views."""
import logging

from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer, RegisterSerializer, UserSerializer
from .services import authenticate_user, register_user

logger = logging.getLogger('accounts')

# Session length constants (seconds)
SESSION_SHORT = 60 * 60 * 24          # 1 day
SESSION_LONG = 60 * 60 * 24 * 30      # 30 days


class RegisterView(APIView):
    """POST /api/auth/register/ — create account & auto-login."""

    permission_classes = [AllowAny]
    authentication_classes = []        # No auth required for registration

    def post(self, request: Request) -> Response:
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'success': False, 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = register_user(serializer.validated_data)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            request.session.set_expiry(SESSION_SHORT)

            return Response(
                {
                    'success': True,
                    'message': 'Account created successfully.',
                    'data': {
                        'user': UserSerializer(user).data,
                        'redirect': '/03-onboarding/index.html',
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception:
            logger.exception('Registration failed')
            return Response(
                {'success': False, 'message': 'Something went wrong.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LoginView(APIView):
    """POST /api/auth/login/ — authenticate & create session."""

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'success': False, 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate_user(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
        )

        if user is None:
            return Response(
                {'success': False, 'errors': {'email': ['Invalid email or password.']}},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.is_active:
            return Response(
                {'success': False, 'errors': {'email': ['This account has been deactivated.']}},
                status=status.HTTP_403_FORBIDDEN,
            )

        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        # Remember-me: long session vs short session
        remember = serializer.validated_data.get('remember_me', False)
        request.session.set_expiry(SESSION_LONG if remember else SESSION_SHORT)

        # Determine redirect target
        redirect_url = (
            '/04-dashboard/dashboard.html'
            if user.onboarding_completed
            else '/03-onboarding/index.html'
        )

        return Response(
            {
                'success': True,
                'message': 'Login successful.',
                'data': {
                    'user': UserSerializer(user).data,
                    'redirect': redirect_url,
                },
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    """POST /api/auth/logout/ — destroy session."""

    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        logger.info('User logged out: %s', request.user.email)
        logout(request)
        return Response(
            {
                'success': True,
                'message': 'Logged out successfully.',
                'data': {'redirect': '/01-landing-page/index.html'},
            },
            status=status.HTTP_200_OK,
        )


class UserView(APIView):
    """GET /api/auth/user/ — return current authenticated user."""

    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        return Response(
            {
                'success': True,
                'data': UserSerializer(request.user).data,
            },
            status=status.HTTP_200_OK,
        )
