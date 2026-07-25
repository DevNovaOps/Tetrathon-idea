"""
Groq Client — reusable wrapper around the Groq SDK.
All LLM interactions go through this single service.
"""
import logging
from django.conf import settings
from groq import Groq
from .prompt_templates import SYSTEM_PROMPT

logger = logging.getLogger('ai_assistant')


class GroqService:
    """Singleton-pattern Groq API client."""

    _client = None
    MODEL = "llama-3.3-70b-versatile"

    @classmethod
    def _get_client(cls) -> Groq:
        if cls._client is None:
            api_key = getattr(settings, 'GROQ_API_KEY', '')
            if not api_key:
                raise ValueError("GROQ_API_KEY is not configured in settings.")
            cls._client = Groq(api_key=api_key)
        return cls._client

    @classmethod
    def chat(cls, user_prompt: str, temperature: float = 0.4, max_tokens: int = 500) -> str:
        """Send a single prompt to Groq and return the assistant's response text."""
        try:
            client = cls._get_client()
            response = client.chat.completions.create(
                model=cls.MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            content = response.choices[0].message.content
            logger.info(f"Groq response received ({len(content)} chars)")
            return content.strip()
        except ValueError:
            raise
        except Exception as e:
            logger.exception(f"Groq API error: {e}")
            return cls._fallback_response()

    @classmethod
    def generate_summary(cls, prompt: str) -> str:
        """Generate a comprehensive financial summary using a higher token limit."""
        return cls.chat(prompt, temperature=0.3, max_tokens=800)

    @staticmethod
    def _fallback_response() -> str:
        return "I appreciate your patience. Let me continue with the next question."
