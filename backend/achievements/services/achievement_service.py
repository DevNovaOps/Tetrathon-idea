from achievements.models import Achievement, Badge, UserLevel
from achievements.services.badge_service import BadgeService
from achievements.services.statistics_service import StatisticsService
from django.utils import timezone

class AchievementService:
    @staticmethod
    def get_summary_data(user):
        BadgeService.seed_default_badges()
        
        if not user or not user.is_authenticated:
            return {
                "unlocked_count": 12,
                "completion_pct": "60%",
                "current_level": "Intermediate",
                "current_streak": "14 Days"
            }

        unlocked_count = Achievement.objects.filter(user=user, unlocked=True).count()
        total_badges = Badge.objects.count()
        if total_badges == 0:
            pct = 0
        else:
            pct = round((unlocked_count / total_badges) * 100)

        level_obj, _ = UserLevel.objects.get_or_create(user=user)
        level_obj.update_level()
        level_obj.save()

        return {
            "unlocked_count": unlocked_count,
            "completion_pct": f"{pct}%",
            "current_level": level_obj.current_level,
            "current_streak": f"{level_obj.current_streak} Days"
        }

    @staticmethod
    def get_unlocked_grid(user):
        BadgeService.seed_default_badges()
        
        if not user or not user.is_authenticated:
            return AchievementService._demo_unlocked_grid()

        achievements = Achievement.objects.filter(user=user, unlocked=True).select_related("badge")
        if not achievements.exists():
            # If user has no achievements unlocked yet, unlock default starter ones for great UX
            AchievementService._unlock_starter_achievements(user)
            achievements = Achievement.objects.filter(user=user, unlocked=True).select_related("badge")

        result = []
        for ach in achievements:
            b = ach.badge
            item = {
                "id": str(ach.id),
                "badge_id": str(b.id),
                "title": b.title,
                "description": b.description,
                "icon": b.icon,
                "xp": b.xp,
                "unlocked": True,
                "unlocked_at": ach.unlocked_at.strftime("%Y-%m-%d") if ach.unlocked_at else "Recently",
                "progress": ach.progress,
                "required_progress": ach.required_progress
            }
            result.append(item)
        return result

    @staticmethod
    def get_locked_milestones(user):
        BadgeService.seed_default_badges()
        
        if not user or not user.is_authenticated:
            return AchievementService._demo_locked_milestones()

        milestone_badges = Badge.objects.filter(is_milestone=True)
        result = []
        for b in milestone_badges:
            ach, _ = Achievement.objects.get_or_create(
                user=user, badge=b,
                defaults={"required_progress": b.target_value, "progress": 0.0}
            )
            if not ach.unlocked:
                pct = round((ach.progress / ach.required_progress) * 100)
                if pct > 100:
                    pct = 100
                
                # Format progress text nicely
                if "₹" in b.title or "Portfolio" in b.title:
                    prog_text = f"₹{int(ach.progress):,} / ₹{int(ach.required_progress):,}"
                elif "Days" in b.title or "Consistency" in b.title:
                    prog_text = f"{int(ach.progress)} / {int(ach.required_progress)} Days"
                elif "Score" in b.title:
                    prog_text = f"{int(ach.progress)} / {int(ach.required_progress)}"
                else:
                    prog_text = f"{int(ach.progress)} / {int(ach.required_progress)}"

                result.append({
                    "id": str(ach.id),
                    "badge_id": str(b.id),
                    "title": b.title,
                    "description": b.description,
                    "icon": "🔒",
                    "xp": b.xp,
                    "progress": ach.progress,
                    "required_progress": ach.required_progress,
                    "progress_pct": pct,
                    "progress_text": prog_text
                })
        return result

    @staticmethod
    def get_explainable_ai_insight(user, achievement_id):
        try:
            ach = Achievement.objects.select_related("badge").get(id=achievement_id)
            b = ach.badge
        except Achievement.DoesNotExist:
            return {
                "title": "Achievement Insight",
                "status": "In Progress",
                "explanation": "This achievement unlocks as you maintain healthy financial habits across Finora.",
                "action_steps": ["Complete lessons in the Learn section", "Keep your credit utilization below 30%", "Log your investments regularly"]
            }

        status = "Unlocked 🎉" if ach.unlocked else "In Progress ⏳"
        
        # Deterministic Explainable AI rules
        if ach.unlocked:
            explanation = (
                f"You successfully achieved '{b.title}' by reaching the target requirement of {b.target_value}. "
                f"Our deterministic AI tracking engine verified this financial milestone from your activity, awarding you +{b.xp} XP."
            )
            action_steps = [
                "Maintain this positive habit to unlock advanced milestones",
                f"You gained +{b.xp} XP towards your overall Level progression",
                "Check the Next Milestones section for your next target"
            ]
        else:
            remaining = max(0, b.target_value - ach.progress)
            explanation = (
                f"You are currently at {int(ach.progress)} / {int(b.target_value)} for '{b.title}'. "
                f"Our AI progression tracker estimates you need {int(remaining)} more units to complete this milestone and earn +{b.xp} XP."
            )
            if "Credit" in b.title:
                action_steps = [
                    "Pay off outstanding credit card balances before the due date",
                    "Keep your credit utilization ratio strictly under 30%",
                    "Avoid applying for multiple new credit cards within a short period"
                ]
            elif "Lesson" in b.title or "Bookworm" in b.title or "Streak" in b.title:
                action_steps = [
                    "Visit the Learn section and complete at least 1 lesson today",
                    "Score 100% on interactive quizzes to reinforce concepts",
                    "Maintain a daily learning streak to accelerate XP growth"
                ]
            elif "Portfolio" in b.title or "Investment" in b.title:
                action_steps = [
                    "Automate a monthly SIP contribution to grow compounding returns",
                    "Diversify across equity mutual funds and secure fixed income",
                    "Use the Growth Simulator to forecast your long-term wealth targets"
                ]
            else:
                action_steps = [
                    f"Perform actions related to {b.title} in the dashboard",
                    "Stay consistent with your monthly budget and savings goals",
                    "Review your financial reports monthly to track your trajectory"
                ]

        return {
            "title": b.title,
            "badge_icon": b.icon,
            "status": status,
            "xp_reward": b.xp,
            "progress_text": f"{int(ach.progress)} / {int(b.target_value)}",
            "progress_pct": min(100, round((ach.progress / max(1, b.target_value)) * 100)),
            "explanation": explanation,
            "action_steps": action_steps
        }

    @staticmethod
    def _unlock_starter_achievements(user):
        starter_rules = ["first_lesson", "bookworm", "first_investment", "profile_completed", "first_ai_assessment"]
        for r in starter_rules:
            b = BadgeService.get_badge_by_rule(r)
            if b:
                Achievement.objects.get_or_create(
                    user=user, badge=b,
                    defaults={"unlocked": True, "unlocked_at": timezone.now(), "progress": b.target_value, "required_progress": b.target_value}
                )

    @staticmethod
    def _demo_unlocked_grid():
        return [
            {"id": "1", "title": "First Investment", "description": "Made your first investment", "icon": "📊", "unlocked": True},
            {"id": "2", "title": "7-Day Savings", "description": "Saved money for 7 consecutive days", "icon": "💰", "unlocked": True},
            {"id": "3", "title": "Completed Profile", "description": "Filled in all profile details", "icon": "📖", "unlocked": True},
            {"id": "4", "title": "First AI Assessment", "description": "Completed your first AI review", "icon": "🤖", "unlocked": True},
            {"id": "5", "title": "Budget Master", "description": "Stayed within budget for 3 months", "icon": "🏆", "unlocked": True},
            {"id": "6", "title": "7-Day Learning Streak", "description": "Completed lessons 7 days in a row", "icon": "🔥", "unlocked": True},
            {"id": "7", "title": "Smart Saver", "description": "Saved 20%+ of income for 3 months", "icon": "💎", "unlocked": True},
            {"id": "8", "title": "Finance Explorer", "description": "Explored all Finora features", "icon": "🚀", "unlocked": True},
        ]

    @staticmethod
    def _demo_locked_milestones():
        return [
            {"id": "101", "title": "Credit Score 800+", "description": "Reach a credit score of 800 or above.", "icon": "🔒", "progress_pct": 91, "progress_text": "730 / 800"},
            {"id": "102", "title": "Complete 50 Lessons", "description": "Finish 50 educational lessons.", "icon": "🔒", "progress_pct": 36, "progress_text": "18 / 50"},
            {"id": "103", "title": "30-Day Consistency", "description": "Stay active for 30 consecutive days.", "icon": "🔒", "progress_pct": 47, "progress_text": "14 / 30 Days"},
            {"id": "104", "title": "₹5L Portfolio", "description": "Grow your portfolio to ₹5,00,000.", "icon": "🔒", "progress_pct": 40, "progress_text": "₹2L / ₹5L"},
            {"id": "105", "title": "Investment Journey", "description": "Complete the full investment journey.", "icon": "🔒", "progress_pct": 65, "progress_text": "65% Done"},
        ]
