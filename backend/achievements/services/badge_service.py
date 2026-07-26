from achievements.models import Badge

class BadgeService:
    @staticmethod
    def get_all_badges():
        return Badge.objects.all()

    @staticmethod
    def get_badge_by_rule(rule):
        try:
            return Badge.objects.get(unlock_rule=rule)
        except Badge.DoesNotExist:
            return None

    @staticmethod
    def seed_default_badges():
        default_badges = [
            {"rule": "first_lesson", "title": "First Lesson", "desc": "Completed your first educational lesson", "icon": "🏅", "xp": 20, "target": 1, "milestone": False},
            {"rule": "bookworm", "title": "Bookworm", "desc": "Completed 5 educational lessons", "icon": "📖", "xp": 30, "target": 5, "milestone": False},
            {"rule": "7_day_streak", "title": "7-Day Streak", "desc": "Completed lessons 7 days in a row", "icon": "🔥", "xp": 50, "target": 7, "milestone": False},
            {"rule": "course_master", "title": "Course Master", "desc": "Completed your first full course", "icon": "🏆", "xp": 100, "target": 1, "milestone": False},
            {"rule": "finance_pro", "title": "Finance Pro", "desc": "Completed 3 full financial courses", "icon": "🎖️", "xp": 150, "target": 3, "milestone": False},
            {"rule": "master_personal_finance", "title": "Master Personal Finance Mastered!", "desc": "Completed 100% of Master Personal Finance course", "icon": "🎓", "xp": 300, "target": 1, "milestone": False},
            {"rule": "first_investment", "title": "First Investment", "desc": "Made your first investment", "icon": "📊", "xp": 25, "target": 1, "milestone": False},
            {"rule": "7_day_savings", "title": "7-Day Savings", "desc": "Saved money for 7 consecutive days", "icon": "💰", "xp": 30, "target": 7, "milestone": False},
            {"rule": "credit_improved", "title": "Credit Score Improved", "desc": "Increased score by 50+ points", "icon": "🛡️", "xp": 40, "target": 50, "milestone": False},
            {"rule": "savings_goal", "title": "Savings Goal", "desc": "Saved ₹10,000", "icon": "🏠", "xp": 50, "target": 10000, "milestone": False},
            {"rule": "investment_streak", "title": "Investment Streak", "desc": "Invested for 3 months", "icon": "📈", "xp": 45, "target": 3, "milestone": False},
            {"rule": "profile_completed", "title": "Completed Profile", "desc": "Filled in all profile details", "icon": "📖", "xp": 20, "target": 1, "milestone": False},
            {"rule": "first_ai_assessment", "title": "First AI Assessment", "desc": "Completed your first AI review", "icon": "🤖", "xp": 25, "target": 1, "milestone": False},
            {"rule": "budget_master", "title": "Budget Master", "desc": "Stayed within budget for 3 months", "icon": "🏆", "xp": 50, "target": 3, "milestone": False},
            {"rule": "smart_saver", "title": "Smart Saver", "desc": "Saved 20%+ of income for 3 months", "icon": "💎", "xp": 50, "target": 3, "milestone": False},
            {"rule": "finance_explorer", "title": "Finance Explorer", "desc": "Explored all Finora features", "icon": "🚀", "xp": 60, "target": 1, "milestone": False},
            # Locked milestones
            {"rule": "credit_score_800", "title": "Credit Score 800+", "desc": "Reach a credit score of 800 or above.", "icon": "🔒", "xp": 100, "target": 800, "milestone": True},
            {"rule": "complete_50_lessons", "title": "Complete 50 Lessons", "desc": "Finish 50 educational lessons.", "icon": "🔒", "xp": 200, "target": 50, "milestone": True},
            {"rule": "30_day_consistency", "title": "30-Day Consistency", "desc": "Stay active for 30 consecutive days.", "icon": "🔒", "xp": 150, "target": 30, "milestone": True},
            {"rule": "5l_portfolio", "title": "₹5L Portfolio", "desc": "Grow your portfolio to ₹5,00,000.", "icon": "🔒", "xp": 250, "target": 500000, "milestone": True},
            {"rule": "investment_journey", "title": "Investment Journey", "desc": "Complete the full investment journey.", "icon": "🔒", "xp": 300, "target": 100, "milestone": True},
        ]

        created_count = 0
        for b in default_badges:
            badge, created = Badge.objects.get_or_create(
                unlock_rule=b["rule"],
                defaults={
                    "title": b["title"],
                    "description": b["desc"],
                    "icon": b["icon"],
                    "xp": b["xp"],
                    "target_value": b["target"],
                    "is_milestone": b["milestone"]
                }
            )
            if created:
                created_count += 1
        return created_count
