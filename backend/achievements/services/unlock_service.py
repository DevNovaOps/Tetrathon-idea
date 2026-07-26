from achievements.models import Achievement, Badge
from achievements.services.badge_service import BadgeService
from achievements.services.reward_service import RewardService
from django.utils import timezone

class UnlockService:
    @staticmethod
    def check_and_unlock(user, event_type, value=1.0, specific_rule=None):
        if not user or not user.is_authenticated:
            return []

        BadgeService.seed_default_badges()
        unlocked_list = []

        # Map event_type to potential badge rules
        rules_to_check = []
        if specific_rule:
            rules_to_check = [specific_rule]
        elif event_type == "lesson_completed":
            rules_to_check = ["first_lesson", "bookworm", "complete_50_lessons"]
        elif event_type == "course_completed":
            rules_to_check = [
                "course_master", "finance_pro", "master_personal_finance",
                "module_credit_score", "module_mutual_funds", "module_sips",
                "module_emergency_fund", "module_financial_literacy", "module_budgeting",
                "module_stock_market", "module_tax_planning", "module_financial_security"
            ]
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

    @staticmethod
    def sync_course_badges(user):
        if not user or not user.is_authenticated:
            return []
        from learning.models import Course, UserProgress
        cat_to_rule = {
            "What is Credit Score?": "module_credit_score",
            "Mutual Funds": "module_mutual_funds",
            "SIPs": "module_sips",
            "Emergency Fund": "module_emergency_fund",
            "Financial Literacy": "module_financial_literacy",
            "Budgeting": "module_budgeting",
            "Stock Market Basics": "module_stock_market",
            "Tax Planning": "module_tax_planning",
            "Financial Security": "module_financial_security",
            "Featured Course": "master_personal_finance",
        }
        unlocked_any = []
        completed_courses_count = 0
        for course in Course.objects.all():
            total_l = course.lessons.count()
            if total_l == 0:
                continue
            user_l = UserProgress.objects.filter(user=user, course=course, completed=True).count()
            if user_l >= total_l:
                completed_courses_count += 1
                rule = cat_to_rule.get(course.category)
                if rule:
                    res = UnlockService.check_and_unlock(user, "specific_rule", 1, specific_rule=rule)
                    unlocked_any.extend(res)
        if completed_courses_count >= 1:
            unlocked_any.extend(UnlockService.check_and_unlock(user, "specific_rule", 1, specific_rule="course_master"))
        if completed_courses_count >= 3:
            unlocked_any.extend(UnlockService.check_and_unlock(user, "specific_rule", 1, specific_rule="finance_pro"))
        return unlocked_any
