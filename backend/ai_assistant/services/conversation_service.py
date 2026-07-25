from typing import Tuple, Optional
from django.db import transaction
from .groq_client import GroqService
from .prompt_templates import QUESTIONS, get_system_prompt, generate_transition_prompt
from .assessment_service import AssessmentService
from ..models import Conversation, ConversationMessage, AssessmentAnswer

class ConversationService:
    
    @staticmethod
    def get_or_create_active_conversation(user) -> Conversation:
        conversation = Conversation.objects.filter(user=user, completed=False).order_by('-started_at').first()
        if not conversation:
            conversation = Conversation.objects.create(user=user)
        return conversation

    @staticmethod
    @transaction.atomic
    def start_conversation(user) -> dict:
        """Starts a new conversation, dropping any incomplete ones."""
        Conversation.objects.filter(user=user, completed=False).delete()
        conversation = Conversation.objects.create(user=user)
        
        greeting = "Hi there! 👋\n\nI'm Finora, your AI Financial Assistant. Let's understand your financial profile before generating your personalized investment recommendation."
        
        # Save greeting
        ConversationMessage.objects.create(
            conversation=conversation,
            role='assistant',
            content=greeting
        )
        
        # Ask first question
        q1 = QUESTIONS[0]
        ConversationMessage.objects.create(
            conversation=conversation,
            role='assistant',
            content=q1['question'],
            choices=q1['choices']
        )
        
        return {
            "completed": False,
            "assistant_message": greeting,
            "question": q1['question'],
            "choices": q1['choices'],
            "step": 1,
            "progress": int((1 / len(QUESTIONS)) * 100)
        }

    @staticmethod
    @transaction.atomic
    def process_message(user, answer: str) -> dict:
        conversation = Conversation.objects.filter(user=user, completed=False).order_by('-started_at').first()
        if not conversation:
            raise ValueError("No active conversation found. Please start over.")

        # Ensure we don't process beyond questions length
        current_step_idx = conversation.current_step - 1
        if current_step_idx >= len(QUESTIONS):
            raise ValueError("Conversation already at final step.")

        current_q = QUESTIONS[current_step_idx]
        
        # Save User Answer message
        ConversationMessage.objects.create(
            conversation=conversation,
            role='user',
            content=answer
        )
        
        # Save specific assessment datapoint
        AssessmentAnswer.objects.create(
            conversation=conversation,
            question_key=current_q['key'],
            question=current_q['question'],
            answer=answer
        )
        
        # Advance step
        conversation.current_step += 1
        conversation.save(update_fields=['current_step'])
        
        # Check if done
        if conversation.current_step > len(QUESTIONS):
            # Finalize Assessment
            return AssessmentService.finalize_assessment(conversation)
            
        # Ask next question using Groq for transition
        next_q = QUESTIONS[conversation.current_step - 1]
        
        groq_client = GroqService()
        messages = [
            {"role": "system", "content": get_system_prompt()},
            {"role": "user", "content": generate_transition_prompt(answer, next_q['question'])}
        ]
        
        ai_response = groq_client.chat(messages)
        
        # Save Assistant message
        ConversationMessage.objects.create(
            conversation=conversation,
            role='assistant',
            content=ai_response,
            choices=next_q['choices']
        )
        
        return {
            "completed": False,
            "assistant_message": ai_response,
            "question": next_q['question'],
            "choices": next_q['choices'],
            "step": conversation.current_step,
            "progress": int((conversation.current_step / len(QUESTIONS)) * 100)
        }
