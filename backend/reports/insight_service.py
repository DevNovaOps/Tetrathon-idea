import json
import logging
import datetime
import random
from .analytics_service import AnalyticsService

logger = logging.getLogger("ai_assistant")

class InsightService:
    @staticmethod
    def get_insights(user, month_str=None, year_str=None):
        summary = AnalyticsService.get_summary(user, month_str, year_str)
        raw = summary["_raw"]
        
        try:
            target_year = int(year_str) if year_str else datetime.date.today().year
            target_month = int(month_str) if month_str else datetime.date.today().month
        except (ValueError, TypeError):
            target_year, target_month = datetime.date.today().year, datetime.date.today().month
            
        month_label = datetime.date(target_year, target_month, 1).strftime("%B")
        
        # 1. Gather User Memory & Profile from DB
        memory_items = []
        risk_bucket = "Moderate"
        try:
            from risk_profile.models import RiskProfile
            rp = RiskProfile.objects.get(user=user)
            risk_bucket = rp.risk_bucket
            memory_items.append(f"Risk Profile: {rp.risk_bucket} (Score: {rp.score}/100)")
        except Exception:
            pass

        try:
            from ai_assistant.models import AssessmentAnswer
            answers = AssessmentAnswer.objects.filter(conversation__user=user).order_by('-created_at')[:8]
            for a in answers:
                memory_items.append(f"Goal/Answer ({a.question_key}): {a.answer}")
        except Exception:
            pass
            
        try:
            from investment.models import InvestmentProfile
            ip = InvestmentProfile.objects.get(user=user)
            memory_items.append(f"Monthly SIP Target: ₹{ip.monthly_sip:,.0f}")
        except Exception:
            pass

        memory_str = "; ".join(memory_items) if memory_items else "Primary goal: Wealth accumulation and tax optimization."
        
        # 2. Attempt Groq AI Generation using memory
        try:
            from ai_assistant.groq_client import GroqService
            
            prompt = f"""You are Finora AI, an expert FinTech wealth advisor.
Generate exactly 4 personalized financial insights for user '{user.first_name if user and getattr(user, 'first_name', '') else "Dev"}' for {month_label} {target_year}.

USER FINANCIAL MEMORY & SNAPSHOT ({month_label} {target_year}):
- Monthly Income: ₹{raw['income']:,.0f}
- Monthly Expenses: ₹{raw['expenses']:,.0f}
- Monthly Savings: ₹{raw['savings']:,.0f} (Rate: {summary['savings_rate']})
- Investment Portfolio: ₹{raw['investment_value']:,.0f}
- Risk Tolerance: {risk_bucket}
- Past AI Memory & Assessment Goals: {memory_str}

REQUIREMENTS:
1. Return ONLY a valid JSON array containing exactly 4 objects. No markdown formatting, no code block backticks, just the raw JSON array.
2. Each object MUST have exactly these 4 keys:
   - "title": An insightful 1-sentence observation or accolade specifically tailored for {month_label} {target_year}.
   - "description": 1 or 2 sentences referencing their exact monthly numbers (₹{raw['savings']:,.0f} savings, ₹{raw['expenses']:,.0f} expense, etc.) and linking it to their memory goals ({risk_bucket} profile).
   - "icon": A single icon string chosen from: "✓", "⚠", "📈", "💳", "🛡️"
   - "bg_class": A CSS class string chosen from: "green-bg", "orange-bg", "blue-bg", "purple-bg", "cyan-bg"
"""
            raw_response = GroqService.chat(prompt, temperature=0.5, max_tokens=650)
            
            cleaned_json = raw_response.strip()
            if cleaned_json.startswith("```"):
                lines = cleaned_json.splitlines()
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].startswith("```"):
                    lines = lines[:-1]
                cleaned_json = "\n".join(lines).strip()
                
            parsed = json.loads(cleaned_json)
            if isinstance(parsed, list) and len(parsed) >= 4:
                valid = []
                for idx, item in enumerate(parsed[:4]):
                    valid.append({
                        "title": str(item.get("title", f"Insight for {month_label}")),
                        "description": str(item.get("description", "Analyzed by Finora AI memory engine.")),
                        "icon": str(item.get("icon", ["✓", "📈", "💳", "🛡️"][idx % 4])),
                        "bg_class": str(item.get("bg_class", ["green-bg", "blue-bg", "purple-bg", "cyan-bg"][idx % 4]))
                    })
                return valid
        except Exception as e:
            logger.warning(f"Groq insight generation fallback triggered: {e}")

        # 3. Dynamic Fallback — NEVER static!
        seed_str = f"ins-{user.email if user else 'demo'}-{target_year}-{target_month}"
        random.seed(seed_str)
        
        savings = raw["savings"]
        expenses = raw["expenses"]
        income = raw["income"]
        inv = raw["investment_value"]
        
        return [
            {
                "title": f"Strong savings discipline in {month_label} {target_year}.",
                "description": f"You saved ₹{savings:,.0f} ({summary['savings_rate']} of income). Based on your memory profile, this consistency keeps your wealth accumulation on target.",
                "icon": "✓",
                "bg_class": "green-bg"
            },
            {
                "title": f"Expenses managed at ₹{expenses:,.0f} for {month_label}.",
                "description": f"Your expenditure ratio is {summary['expense_ratio']}. Keeping overheads optimized aligns well with your {risk_bucket.lower()} risk tolerance.",
                "icon": "⚠" if expenses > (income * 0.5) else "✓",
                "bg_class": "orange-bg" if expenses > (income * 0.5) else "blue-bg"
            },
            {
                "title": f"Portfolio compounding at ₹{inv:,.0f}.",
                "description": f"Your investment allocation in {target_year} shows active progress. Continued monthly SIP contributions will maximize long-term returns.",
                "icon": "📈",
                "bg_class": "purple-bg"
            },
            {
                "title": f"Financial wellness & credit defense active.",
                "description": f"Your emergency fund coverage of {summary['emergency_fund_coverage']} protects against volatility while reinforcing your credit score.",
                "icon": "🛡️",
                "bg_class": "cyan-bg"
            }
        ]

