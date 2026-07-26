from learning.models import Course, Article, AiTip

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
            # Recommend risk management, diversification, emergency fund
            c = Course.objects.filter(category__in=["Emergency Fund", "Financial Security", "Mutual Funds"]).all()
            rec_courses.extend(c)
        elif credit_score_val < 750:
            # Recommend credit score improvement
            c = Course.objects.filter(category__in=["What is Credit Score?", "Budgeting", "Financial Literacy"]).all()
            rec_courses.extend(c)
        else:
            # Recommend wealth growth and tax planning
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
        articles = Article.objects.all()[:5]
        return [
            {
                "id": str(a.id),
                "title": a.title,
                "tag": a.tag,
                "tag_color": a.tag_color,
                "summary": a.summary,
                "read_time": a.read_time,
                "difficulty": a.difficulty
            }
            for a in articles
        ]

    @staticmethod
    def get_ai_learning_tips(user):
        tips = AiTip.objects.all()[:4]
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
