from achievements.models import Achievement, Badge
from achievements.services.badge_service import BadgeService
from achievements.services.reward_service import RewardService
from django.utils import timezone

class UnlockService:
    @staticmethod
    def check_and_unlock(user, event_type, value=1.0):
        if not user or not user.is_authenticated:
            return []

        BadgeService.seed_default_badges()
        unlocked_list = []

        # Map event_type to potential badge rules
        rules_to_check = []
        if event_type == "lesson_completed":
            rules_to_check = ["first_lesson", "bookworm", "complete_50_lessons"]
        elif event_type == "course_completed":
            rules_to_check = ["course_master", "finance_pro", "master_personal_finance"]
        elif event_type == "report_downloaded":
            rules_to_check = ["report_reader"]
        elif event_type == "investment_added":
            rules_to_check = ["first_investment", "investment_streak", "investment_journey"]
        elif event_type == "portfolio_updated":
            rules_to_check = ["5l_portfolio"]
        elif event_type == "credit_improved" or event_type == "credit_updated":
            rules_to_check = ["credit_improved", "credit_score_800"]
        elif event_type == "simulator_run":
            rules_to_check = ["simulator_expert", "finance_explorer"]
        elif event_type == "goal_created" or event_type == "savings_updated":
            rules_to_check = ["savings_goal", "7_day_savings", "smart_saver"]
        elif event_type == "ai_assessment":
            rules_to_check = ["first_ai_assessment", "ai_explorer"]
        elif event_type == "profile_completed":
            rules_to_check = ["profile_completed"]
        elif event_type == "streak_updated":
            rules_to_check = ["7_day_streak", "30_day_consistency"]

        for rule in rules_to_check:
            badge = BadgeService.get_badge_by_rule(rule)
            if not badge:
                continue

            ach, created = Achievement.objects.get_or_create(
                user=user, badge=badge,
                defaults={"required_progress": badge.target_value, "progress": 0.0}
            )

            if ach.unlocked:
                continue

            # Update progress
            if rule in ["5l_portfolio", "credit_score_800"]:
                # Absolute target value e.g. portfolio value or credit score
                ach.progress = float(value)
            else:
                # Incremental progress
                ach.progress += float(value)

            if ach.progress >= ach.required_progress:
                ach.progress = ach.required_progress
                ach.unlocked = True
                ach.unlocked_at = timezone.now()
                ach.save()

                # Award XP for unlocking achievement!
                RewardService.award_xp(user, badge.xp, reason=f"Unlocked Achievement: {badge.title}")

                unlocked_list.append({
                    "badge_id": str(badge.id),
                    "title": badge.title,
                    "description": badge.description,
                    "icon": badge.icon,
                    "xp": badge.xp,
                    "unlocked_at": ach.unlocked_at.strftime("%Y-%m-%d %H:%M:%S")
                })
            else:
                ach.save()

        return unlocked_list
