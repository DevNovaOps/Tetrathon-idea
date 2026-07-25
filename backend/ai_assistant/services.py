"""
Service Layer for the AI Assistant module.
Orchestrates conversation flow, Groq calls, risk engine, and recommendation engine.
"""
import logging
from django.db import transaction
from .models import Conversation, ConversationMessage, AssessmentAnswer
from .groq_client import GroqService
from .conversation_manager import get_question, get_progress, TOTAL_QUESTIONS
from .risk_engine import RiskEngine
from .recommendation_engine import RecommendationEngine
from .prompt_templates import GREETING_PROMPT, QUESTION_TRANSITION_PROMPT, SUMMARY_PROMPT
from .utils.amount_parser import normalize_amount

logger = logging.getLogger('ai_assistant')


class AssistantService:
    """Orchestrates the full AI assessment conversation lifecycle."""

    @staticmethod
    @transaction.atomic
    def start_conversation(user) -> dict:
        """Creates a new conversation (or resumes an existing incomplete one) and returns the greeting + Q1."""
        # Check for an existing incomplete conversation
        existing = Conversation.objects.filter(user=user, completed=False).first()
        if existing:
            # Resume: return history and current step
            return AssistantService._build_resume_response(existing)

        # Create fresh conversation
        conversation = Conversation.objects.create(user=user, current_step=0)

        # Generate greeting via Groq
        user_name = user.full_name.split(' ')[0] if user.full_name else 'there'
        try:
            greeting_text = GroqService.chat(
                GREETING_PROMPT.format(user_name=user_name)
            )
        except Exception:
            greeting_text = f"Hi {user_name} 👋 Welcome to your financial assessment. I'll ask a few quick questions to understand your financial profile and generate personalized recommendations."

        # Save greeting message
        ConversationMessage.objects.create(
            conversation=conversation, role='assistant', content=greeting_text
        )

        # Get first question
        q = get_question(0)
        question_text = q['question']
        if q.get('type') == 'amount':
            question_text += "\n\n*(You can also type any amount)*"

        ConversationMessage.objects.create(
            conversation=conversation, role='assistant', content=question_text
        )

        return {
            "conversation_id": str(conversation.id),
            "completed": False,
            "assistant_message": greeting_text,
            "question": question_text,
            "chips": q['chips'],
            "step": 1,
            "progress": get_progress(0),
        }

    @staticmethod
    @transaction.atomic
    def process_message(user, answer: str) -> dict:
        """Processes a user's answer, stores it, and returns the next step or assessment."""
        conversation = Conversation.objects.filter(user=user, completed=False).first()
        if not conversation:
            return AssistantService.start_conversation(user)

        current_step = conversation.current_step
        current_q = get_question(current_step)

        if not current_q:
            # Already past all questions — return assessment
            return AssistantService._generate_assessment(conversation)

        # Process answer based on question type
        numeric_value = None
        formatted_answer = answer
        
        if current_q.get('type') == 'amount':
            parsed = normalize_amount(answer)
            if not parsed:
                # Invalid amount, reject and prompt again without advancing
                error_msg = "Please enter a valid amount (e.g., 30000, 30k, 1.5cr, or ₹30,000)."
                q_text = current_q['question']
                if current_q.get('type') == 'amount':
                    q_text += "\n\n*(You can also type any amount)*"
                    
                return {
                    "conversation_id": str(conversation.id),
                    "completed": False,
                    "assistant_message": error_msg,
                    "question": q_text,
                    "chips": current_q['chips'],
                    "step": current_step + 1,
                    "progress": get_progress(current_step),
                    "error": True,
                    "formatted_answer": None
                }
            
            numeric_value = parsed['value']
            formatted_answer = parsed['display']

        # Store user message (using formatted answer if applicable)
        ConversationMessage.objects.create(
            conversation=conversation, role='user', content=formatted_answer
        )

        # Store assessment answer
        AssessmentAnswer.objects.create(
            conversation=conversation,
            question_key=current_q['key'],
            question=current_q['question'],
            answer=formatted_answer,
            numeric_value=numeric_value,
            weight=current_q['weight'],
        )

        # Advance step
        next_step = current_step + 1
        conversation.current_step = next_step
        conversation.save(update_fields=['current_step'])

        # Check if we have more questions
        next_q = get_question(next_step)
        if next_q:
            # Generate natural transition via Groq using the formatted answer
            try:
                transition = GroqService.chat(
                    QUESTION_TRANSITION_PROMPT.format(
                        previous_answer=formatted_answer,
                        previous_topic=current_q['topic'],
                        next_topic=next_q['topic'],
                    )
                )
            except Exception:
                transition = f"Got it. Now, {next_q['question']}"

            # Save assistant message
            ConversationMessage.objects.create(
                conversation=conversation, role='assistant', content=transition
            )

            next_q_text = next_q['question']
            if next_q.get('type') == 'amount':
                next_q_text += "\n\n*(You can also type any amount)*"

            return {
                "conversation_id": str(conversation.id),
                "completed": False,
                "assistant_message": transition,
                "question": next_q_text,
                "chips": next_q['chips'],
                "step": next_step + 1,
                "progress": get_progress(next_step),
                "formatted_answer": formatted_answer
            }
        else:
            # All questions answered — generate assessment
            result = AssistantService._generate_assessment(conversation)
            result["formatted_answer"] = formatted_answer
            return result

    @staticmethod
    @transaction.atomic
    def _generate_assessment(conversation: Conversation) -> dict:
        """Runs the deterministic risk engine, recommendation engine, and Groq summary."""
        # Collect all answers
        answers = {}
        for a in conversation.answers.all():
            answers[a.question_key] = a.answer

        # Deterministic risk calculation
        risk_result = RiskEngine.calculate(answers)
        risk_score = risk_result['score']
        risk_level = risk_result['level']

        # Deterministic investment allocation
        allocation = RecommendationEngine.get_allocation(risk_level)

        # Build profile string for Groq summary
        profile_data = "\n".join([f"- {k.replace('_', ' ').title()}: {v}" for k, v in answers.items()])
        allocation_data = "\n".join([f"- {a['asset']}: {a['percentage']}%" for a in allocation])

        try:
            summary_text = GroqService.generate_summary(
                SUMMARY_PROMPT.format(
                    profile_data=profile_data,
                    risk_score=risk_score,
                    risk_level=risk_level,
                    allocation_data=allocation_data,
                )
            )
        except Exception:
            summary_text = f"Based on your profile, you have a {risk_level} risk tolerance with a score of {risk_score}/100."

        # Save summary message
        ConversationMessage.objects.create(
            conversation=conversation, role='assistant', content=summary_text
        )

        # Update conversation
        conversation.completed = True
        conversation.risk_score = risk_score
        conversation.risk_level = risk_level
        conversation.summary = summary_text
        conversation.save(update_fields=['completed', 'risk_score', 'risk_level', 'summary'])

        # Build the collected answers for the summary panel
        summary_items = []
        for a in conversation.answers.all():
            summary_items.append({"label": a.question.replace("?", "").strip(), "value": a.answer})

        return {
            "conversation_id": str(conversation.id),
            "completed": True,
            "assistant_message": summary_text,
            "step": TOTAL_QUESTIONS + 1,
            "progress": 100,
            "risk_profile": {
                "score": risk_score,
                "level": risk_level,
            },
            "investment_recommendation": {
                "allocation": allocation,
            },
            "summary_items": summary_items,
        }

    @staticmethod
    def get_history(user) -> dict:
        """Returns the complete conversation history for the user."""
        conversation = Conversation.objects.filter(user=user).order_by('-started_at').first()
        if not conversation:
            return {"messages": [], "completed": False, "step": 0}

        messages = []
        for msg in conversation.messages.all():
            messages.append({
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp.strftime("%I:%M %p"),
            })

        summary_items = []
        for a in conversation.answers.all():
            summary_items.append({"label": a.question.replace("?", "").strip(), "value": a.answer})

        result = {
            "conversation_id": str(conversation.id),
            "messages": messages,
            "completed": conversation.completed,
            "step": conversation.current_step + 1,
            "progress": 100 if conversation.completed else get_progress(conversation.current_step),
            "summary_items": summary_items,
        }

        if conversation.completed:
            allocation = RecommendationEngine.get_allocation(conversation.risk_level)
            result["risk_profile"] = {
                "score": conversation.risk_score,
                "level": conversation.risk_level,
            }
            result["investment_recommendation"] = {"allocation": allocation}
            result["assistant_message"] = conversation.summary

        return result

    @staticmethod
    @transaction.atomic
    def reset_conversation(user) -> dict:
        """Deletes all conversations for the user and starts fresh."""
        Conversation.objects.filter(user=user).delete()
        return AssistantService.start_conversation(user)

    @staticmethod
    def _build_resume_response(conversation: Conversation) -> dict:
        """Builds a response to resume an existing incomplete conversation."""
        current_q = get_question(conversation.current_step)
        # Get previous messages for context
        messages = []
        for msg in conversation.messages.all():
            messages.append({
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp.strftime("%I:%M %p"),
            })

        summary_items = []
        for a in conversation.answers.all():
            summary_items.append({"label": a.question.replace("?", "").strip(), "value": a.answer})

        current_q_text = current_q['question'] if current_q else None
        if current_q and current_q.get('type') == 'amount':
            current_q_text += "\n\n*(You can also type any amount)*"

        return {
            "conversation_id": str(conversation.id),
            "completed": False,
            "messages": messages,
            "question": current_q_text,
            "chips": current_q['chips'] if current_q else [],
            "step": conversation.current_step + 1,
            "progress": get_progress(conversation.current_step),
            "summary_items": summary_items,
            "resumed": True,
        }
