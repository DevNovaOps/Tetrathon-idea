from django.db import transaction
from .risk_engine import RiskEngine
from .recommendation_engine import RecommendationEngine
from .groq_client import GroqService
from ..models import ConversationMessage

class AssessmentService:
    @staticmethod
    @transaction.atomic
    def finalize_assessment(conversation) -> dict:
        """
        Executes the final flow: calculates risk, generates summary, completes conversation.
        """
        # Fetch all answers
        answers_qs = conversation.answers.all()
        answers_data = [{"key": a.question_key, "answer": a.answer} for a in answers_qs]
        
        # 1. Deterministic Risk Engine
        risk_profile = RiskEngine(answers_data).calculate()
        conversation.risk_score = risk_profile["score"]
        conversation.risk_level = risk_profile["level"]
        
        # 2. Deterministic Recommendation Engine
        recommendation = RecommendationEngine(risk_profile["level"]).generate()
        conversation.investment_recommendation = recommendation
        
        # 3. LLM Natural Language Summary
        # Build profile data string for LLM
        profile_string = ", ".join([f"{a['key'].replace('_', ' ').title()}: {a['answer']}" for a in answers_data])
        profile_string += f", Calculated Risk Level: {risk_profile['level']}, Calculated Score: {risk_profile['score']}"
        
        groq_client = GroqService()
        ai_summary = groq_client.generate_summary(profile_string)
        conversation.summary = ai_summary
        
        # Mark Complete
        conversation.completed = True
        conversation.save()
        
        # Create final message
        ConversationMessage.objects.create(
            conversation=conversation,
            role='assistant',
            content=ai_summary
        )
        
        return {
            "completed": True,
            "summary": ai_summary,
            "risk_profile": risk_profile,
            "investment_recommendation": recommendation,
            "step": 8,
            "progress": 100
        }
