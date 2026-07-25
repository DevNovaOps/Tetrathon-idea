import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Prefetch
from .services.conversation_service import ConversationService
from .models import Conversation
from .serializers import ConversationSerializer

logger = logging.getLogger(__name__)

class StartConversationAPIView(APIView):
    """POST /api/assistant/start/"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Check if active exists, else start new
            active = Conversation.objects.filter(user=request.user, completed=False).first()
            if active:
                # Need to return the last asked question
                last_msg = active.messages.filter(role='assistant').last()
                from .services.prompt_templates import QUESTIONS
                step = active.current_step
                progress = int((step / len(QUESTIONS)) * 100)
                
                return Response({
                    "success": True,
                    "data": {
                        "completed": False,
                        "assistant_message": last_msg.content if last_msg else "Let's continue.",
                        "question": last_msg.content if last_msg and not last_msg.choices else None,
                        "choices": last_msg.choices if last_msg else None,
                        "step": step,
                        "progress": progress
                    }
                }, status=status.HTTP_200_OK)
            else:
                data = ConversationService.start_conversation(request.user)
                return Response({"success": True, "data": data}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception("Error starting conversation")
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class MessageAPIView(APIView):
    """POST /api/assistant/message/"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        answer = request.data.get('answer')
        if not answer:
            return Response({"success": False, "message": "Answer is required."}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            data = ConversationService.process_message(request.user, answer)
            return Response({"success": True, "data": data}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception("Error processing message")
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class HistoryAPIView(APIView):
    """GET /api/assistant/history/"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            conversation = Conversation.objects.prefetch_related('messages').filter(user=request.user).order_by('-started_at').first()
            if not conversation:
                return Response({"success": True, "data": None}, status=status.HTTP_200_OK)
                
            serializer = ConversationSerializer(conversation)
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ResetAPIView(APIView):
    """POST /api/assistant/reset/"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = ConversationService.start_conversation(request.user)
            return Response({"success": True, "data": data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
