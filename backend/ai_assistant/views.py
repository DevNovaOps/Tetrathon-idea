from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .services import AssistantService
from .serializers import MessageInputSerializer


class StartConversationAPIView(APIView):
    """POST /api/assistant/start/ — Start or resume a conversation."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = AssistantService.start_conversation(request.user)
            return Response({"success": True, "data": data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SendMessageAPIView(APIView):
    """POST /api/assistant/message/ — Send a user answer."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MessageInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"success": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        try:
            data = AssistantService.process_message(request.user, serializer.validated_data['answer'])
            return Response({"success": True, "data": data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ConversationHistoryAPIView(APIView):
    """GET /api/assistant/history/ — Get full conversation history."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            data = AssistantService.get_history(request.user)
            return Response({"success": True, "data": data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ResetConversationAPIView(APIView):
    """POST /api/assistant/reset/ — Delete and restart conversation."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = AssistantService.reset_conversation(request.user)
            return Response({"success": True, "data": data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
