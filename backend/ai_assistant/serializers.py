from rest_framework import serializers
from .models import Conversation, ConversationMessage

class ConversationMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationMessage
        fields = ['role', 'content', 'choices', 'timestamp']

class ConversationSerializer(serializers.ModelSerializer):
    messages = ConversationMessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Conversation
        fields = [
            'id', 'started_at', 'completed', 'current_step', 
            'risk_score', 'risk_level', 'summary', 'investment_recommendation', 'messages'
        ]
