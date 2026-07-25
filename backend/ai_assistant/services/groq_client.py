import os
import logging
from groq import Groq
from django.conf import settings

logger = logging.getLogger(__name__)

class GroqService:
    def __init__(self):
        # Fallback to os.environ if settings doesn't have it
        api_key = getattr(settings, 'GROQ_API_KEY', os.environ.get('GROQ_API_KEY'))
        if not api_key:
            logger.error("Groq API Key not configured.")
        self.client = Groq(api_key=api_key)
        self.model = "llama3-8b-8192" # Or standard llama model

    def chat(self, messages: list, temperature: float = 0.4, max_tokens: int = 500) -> str:
        """Standard chat interface for natural transitions."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Groq Chat Error: {e}")
            return "I apologize, but I'm having trouble processing that right now. Could you please answer the next question?"

    def generate_summary(self, profile_data: dict) -> str:
        """Generates the final natural language summary of the user's financial profile."""
        prompt = f"""
You are Finora, a professional and friendly AI Financial Advisor.
Based ONLY on the following profile, generate a 3-paragraph summary covering:
1. Financial Summary & Strengths
2. Weaknesses & Risk Explanation
3. Personalized Recommendations

Profile:
{profile_data}

Do not invent values. Be direct, professional, and encouraging. Do not mention you are an AI model.
"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
                max_tokens=600,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Groq Summary Error: {e}")
            return "Based on your responses, we have calculated your risk profile and recommended an investment allocation below."
