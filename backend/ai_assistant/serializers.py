from rest_framework import serializers
from .models import Conversation, ConversationMessage, AssessmentAnswer


class ConversationMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationMessage
        fields = ['id', 'role', 'content', 'timestamp']


class AssessmentAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentAnswer
        fields = ['id', 'question_key', 'question', 'answer', 'weight']


class ConversationSerializer(serializers.ModelSerializer):
    messages = ConversationMessageSerializer(many=True, read_only=True)
    answers = AssessmentAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'current_step', 'completed', 'risk_score', 'risk_level', 'summary', 'messages', 'answers', 'started_at']


class MessageInputSerializer(serializers.Serializer):
    answer = serializers.CharField(max_length=500)
