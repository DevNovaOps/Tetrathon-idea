import json
import logging
from django.utils import timezone
import datetime
from learning.models import Course, Article, AiTip, Lesson, UserProgress, LearningStreak

logger = logging.getLogger('learning')

class RecommendationService:
    @staticmethod
    def get_recommendations(user):
        if not user or not user.is_authenticated:
            return RecommendationService._default_recommendations()

        # Check user profiles deterministically
        risk_profile_type = "Moderate"
        credit_score_val = 720

        try:
            from risk_profile.models import UserRiskProfile
            rp = UserRiskProfile.objects.filter(user=user).first()
            if rp and rp.risk_category:
                risk_profile_type = rp.risk_category
        except Exception:
            pass

        try:
            from credit_score.models import UserCreditScore
            cs = UserCreditScore.objects.filter(user=user).first()
            if cs and cs.score:
                credit_score_val = cs.score
        except Exception:
            pass

        rec_courses = []
        if risk_profile_type in ["High", "Aggressive"]:
            c = Course.objects.filter(category__in=["Emergency Fund", "Financial Security", "Mutual Funds"]).all()
            rec_courses.extend(c)
        elif credit_score_val < 750:
            c = Course.objects.filter(category__in=["What is Credit Score?", "Budgeting", "Financial Literacy"]).all()
            rec_courses.extend(c)
        else:
            c = Course.objects.filter(category__in=["SIPs", "Stock Market Basics", "Tax Planning"]).all()
            rec_courses.extend(c)

        if not rec_courses:
            rec_courses = Course.objects.all()[:3]

        return [
            {
                "id": str(c.id),
                "title": c.title,
                "category": c.category,
                "difficulty": c.difficulty,
                "hours": c.estimated_hours,
                "lessons": c.total_lessons,
                "thumbnail": c.thumbnail
            }
            for c in rec_courses[:4]
        ]

    @staticmethod
    def get_recommended_articles(user):
        articles = Article.objects.all()[:6]
        return [
            {
                "id": str(a.id),
                "title": a.title,
                "tag": a.tag,
                "tag_color": a.tag_color,
                "summary": a.summary,
                "read_time": a.read_time,
                "difficulty": a.difficulty,
                "url": a.url or "",
                "content": a.content
            }
            for a in articles
        ]

    @staticmethod
    def get_ai_learning_tips(user):
        if not user or not user.is_authenticated:
            return RecommendationService._get_default_tips()

        # Check if we generated tips for this user recently (within 4 hours)
        user_tips = AiTip.objects.filter(user=user).order_by('-created_at')
        if user_tips.count() >= 4:
            newest = user_tips.first()
            if newest and newest.created_at and (timezone.now() - newest.created_at) < datetime.timedelta(hours=4):
                return [
                    {
                        "id": str(t.id),
                        "title": t.title,
                        "content": t.content,
                        "icon": t.icon,
                        "icon_bg": t.icon_bg,
                        "category": t.category
                    }
                    for t in user_tips[:4]
                ]

        # Generate dynamic tips using Groq based on live database memory!
        try:
            from ai_assistant.groq_client import GroqService
            
            # Gather live database memory
            credit_score = 720
            try:
                from credit_score.models import UserCreditScore
                cs = UserCreditScore.objects.filter(user=user).first()
                if cs and cs.score:
                    credit_score = cs.score
            except Exception:
                pass

            risk_profile = "Moderate"
            try:
                from risk_profile.models import UserRiskProfile
                rp = UserRiskProfile.objects.filter(user=user).first()
                if rp and rp.risk_category:
                    risk_profile = rp.risk_category
            except Exception:
                pass

            lessons_completed = UserProgress.objects.filter(user=user, completed=True).count()
            total_lessons = Lesson.objects.count()
            
            streak = 0
            try:
                streak_obj = LearningStreak.objects.filter(user=user).first()
                if streak_obj:
                    streak = streak_obj.current_streak
            except Exception:
                pass

            level_name = "Beginner"
            xp = 0
            try:
                from achievements.models import UserLevel
                lvl = UserLevel.objects.filter(user=user).first()
                if lvl:
                    level_name = lvl.current_level
                    xp = lvl.xp
            except Exception:
                pass

            inv_count = 0
            try:
                from investment.models import UserInvestment
                inv_count = UserInvestment.objects.filter(user=user).count()
            except Exception:
                pass

            goal_count = 0
            try:
                from onboarding.models import FinancialGoal
                goal_count = FinancialGoal.objects.filter(user=user).count()
            except Exception:
                pass

            prompt = f"""You are Finora's AI Financial Mentor. Analyze this user's live database metrics:
- Credit Score: {credit_score}
- Risk Profile: {risk_profile}
- Learning Level: {level_name} ({xp} XP), Streak: {streak} days
- Lessons Completed: {lessons_completed} / {total_lessons}
- Investments Tracked: {inv_count}, Financial Goals: {goal_count}

Generate 4 personalized, highly relevant AI learning tips based on their actual metrics and behavior.
You MUST respond with ONLY a valid JSON array of 4 objects matching this exact structure:
[
  {{
    "title": "Boost Credit Below 30% Utilization",
    "content": "With your current CIBIL score of {credit_score}, keeping credit card utilization under 30% and automating due dates will push you into the 800+ tier.",
    "icon": "🛡️",
    "icon_bg": "purple-bg",
    "category": "Credit"
  }},
  {{
    "title": "Maintain Your {streak}-Day Streak",
    "content": "You have completed {lessons_completed} lessons! Try finishing 1 more module in 'Mutual Funds' to level up faster.",
    "icon": "🔥",
    "icon_bg": "orange-bg",
    "category": "Learning"
  }}
]
Do not output any markdown code blocks (no ```json). Output ONLY the raw JSON array string."""

            response_text = GroqService.chat(prompt, temperature=0.5, max_tokens=600)
            
            # Clean response text if wrapped in markdown
            clean_text = response_text.strip()
            if clean_text.startswith("```json"):
                clean_text = clean_text[7:]
            if clean_text.startswith("```"):
                clean_text = clean_text[3:]
            if clean_text.endswith("```"):
                clean_text = clean_text[:-3]
            clean_text = clean_text.strip()

            parsed_tips = json.loads(clean_text)
            if isinstance(parsed_tips, list) and len(parsed_tips) >= 4:
                # Save new tips to DB for this user
                AiTip.objects.filter(user=user).delete()
                new_tips = []
                for t in parsed_tips[:4]:
                    tip_obj = AiTip.objects.create(
                        user=user,
                        title=t.get("title", "Smart Learning Tip")[:200],
                        content=t.get("content", "Consistency builds long-term compounding wealth."),
                        icon=t.get("icon", "💡")[:50],
                        icon_bg=t.get("icon_bg", "green-bg")[:50],
                        category=t.get("category", "General")[:100]
                    )
                    new_tips.append({
                        "id": str(tip_obj.id),
                        "title": tip_obj.title,
                        "content": tip_obj.content,
                        "icon": tip_obj.icon,
                        "icon_bg": tip_obj.icon_bg,
                        "category": tip_obj.category
                    })
                return new_tips

        except Exception as e:
            logger.warning(f"Groq dynamic tip generation failed or rate limited: {e}. Falling back to DB tips.")

        return RecommendationService._get_default_tips(user)

    @staticmethod
    def _get_default_tips(user=None):
        tips = AiTip.objects.filter(user=user).order_by('-id')[:4]
        if tips.count() < 4:
            tips = AiTip.objects.filter(user__isnull=True)[:4]
        return [
            {
                "id": str(t.id),
                "title": t.title,
                "content": t.content,
                "icon": t.icon,
                "icon_bg": t.icon_bg,
                "category": t.category
            }
            for t in tips
        ]

    @staticmethod
    def _default_recommendations():
        courses = Course.objects.all()[:4]
        return [
            {
                "id": str(c.id),
                "title": c.title,
                "category": c.category,
                "difficulty": c.difficulty,
                "hours": c.estimated_hours,
                "lessons": c.total_lessons,
                "thumbnail": c.thumbnail
            }
            for c in courses
        ]
