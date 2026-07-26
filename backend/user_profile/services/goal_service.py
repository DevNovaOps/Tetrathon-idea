from django.utils import timezone
from user_profile.models import FinancialGoal, GoalContribution

class GoalService:
    @staticmethod
    def get_goals(user):
        if not user or not user.is_authenticated:
            return FinancialGoal.objects.none()
        return FinancialGoal.objects.filter(user=user, is_deleted=False)

    @staticmethod
    def get_active_primary_goal(user):
        if not user or not user.is_authenticated:
            return None
        goal = FinancialGoal.objects.filter(user=user, is_deleted=False, is_primary=True, status='Active').first()
        if not goal:
            goal = FinancialGoal.objects.filter(user=user, is_deleted=False, status='Active').order_by('-created_at').first()
            if goal:
                goal.is_primary = True
                goal.save()
        return goal

    @staticmethod
    def set_active_primary_goal(user, goal_id):
        if not user or not user.is_authenticated:
            return None
        try:
            goal = FinancialGoal.objects.get(id=goal_id, user=user, is_deleted=False)
            FinancialGoal.objects.filter(user=user, is_deleted=False).update(is_primary=False)
            goal.is_primary = True
            if goal.status == 'Completed':
                goal.status = 'Active'
            goal.save()
            
            # Record timeline event
            from user_profile.services.timeline_service import TimelineService
            TimelineService.record_event(
                user=user,
                event_type="goal_updated",
                title=f"Set Active Goal: {goal.goal_name}",
                description=f"{goal.goal_name} is now your primary target for wealth growth simulations.",
                category="Goals"
            )
            return goal
        except FinancialGoal.DoesNotExist:
            return None

    @staticmethod
    def create_goal(user, data):
        if not user or not user.is_authenticated:
            return {"error": "Authentication required"}

        is_primary = bool(data.get('is_primary', False))
        # If user has no active primary goal, force first goal to be primary
        if not FinancialGoal.objects.filter(user=user, is_deleted=False, is_primary=True).exists():
            is_primary = True

        if is_primary:
            FinancialGoal.objects.filter(user=user, is_deleted=False).update(is_primary=False)

        target = float(data.get('target_amount', 0) or 0)
        current = float(data.get('current_progress', 0) or 0)
        monthly = float(data.get('monthly_contribution', 0) or 0)
        comp_pct = round((current / target * 100), 2) if target > 0 else 0

        goal = FinancialGoal.objects.create(
            user=user,
            goal_name=data.get('goal_name', 'My Goal'),
            goal_type=data.get('goal_type', 'Custom'),
            target_amount=target,
            current_progress=current,
            monthly_contribution=monthly,
            deadline=data.get('deadline') or None,
            priority=data.get('priority', 'Medium'),
            status='Active',
            is_primary=is_primary,
            completion_percentage=min(comp_pct, 100.0)
        )

        # Record timeline event
        from user_profile.services.timeline_service import TimelineService
        TimelineService.record_event(
            user=user,
            event_type="goal_created",
            title=f"Goal Created: {goal.goal_name}",
            description=f"New target set for ₹{target:,.2f} with monthly contributions of ₹{monthly:,.2f}.",
            category="Goals"
        )
        
        # Check if already completed on creation
        GoalService.check_goal_completion(goal)
        return goal

    @staticmethod
    def update_goal(user, goal_id, data):
        if not user or not user.is_authenticated:
            return {"error": "Authentication required"}
        try:
            goal = FinancialGoal.objects.get(id=goal_id, user=user, is_deleted=False)
            if 'is_primary' in data and bool(data['is_primary']):
                FinancialGoal.objects.filter(user=user, is_deleted=False).update(is_primary=False)
                goal.is_primary = True

            for f in ['goal_name', 'goal_type', 'target_amount', 'current_progress', 'monthly_contribution', 'deadline', 'priority', 'status']:
                if f in data and data[f] is not None:
                    setattr(goal, f, data[f])

            if goal.target_amount > 0:
                goal.completion_percentage = min(round((float(goal.current_progress) / float(goal.target_amount) * 100), 2), 100.0)

            goal.save()
            GoalService.check_goal_completion(goal)
            return goal
        except FinancialGoal.DoesNotExist:
            return {"error": "Goal not found"}

    @staticmethod
    def add_contribution(user, goal_id, amount, notes=""):
        if not user or not user.is_authenticated:
            return {"error": "Authentication required"}
        try:
            goal = FinancialGoal.objects.get(id=goal_id, user=user, is_deleted=False)
            amt = float(amount)
            GoalContribution.objects.create(goal=goal, amount=amt, notes=notes)
            
            goal.current_progress = float(goal.current_progress) + amt
            if goal.target_amount > 0:
                goal.completion_percentage = min(round((float(goal.current_progress) / float(goal.target_amount) * 100), 2), 100.0)
            goal.save()

            GoalService.check_goal_completion(goal)
            return goal
        except FinancialGoal.DoesNotExist:
            return {"error": "Goal not found"}

    @staticmethod
    def delete_goal(user, goal_id):
        if not user or not user.is_authenticated:
            return False
        try:
            goal = FinancialGoal.objects.get(id=goal_id, user=user, is_deleted=False)
            goal.is_deleted = True
            goal.save()
            # If we deleted primary, pick another active goal as primary
            if goal.is_primary:
                next_goal = FinancialGoal.objects.filter(user=user, is_deleted=False, status='Active').first()
                if next_goal:
                    next_goal.is_primary = True
                    next_goal.save()
            return True
        except FinancialGoal.DoesNotExist:
            return False

    @staticmethod
    def check_goal_completion(goal):
        if not goal or goal.is_deleted:
            return
        if float(goal.current_progress) >= float(goal.target_amount) and float(goal.target_amount) > 0:
            if goal.status != 'Completed':
                goal.status = 'Completed'
                goal.completion_percentage = 100.0
                goal.save()

                user = goal.user
                # 1. Timeline Event
                from user_profile.services.timeline_service import TimelineService
                TimelineService.record_event(
                    user=user,
                    event_type="goal_completed",
                    title=f"Goal Mastered: {goal.goal_name}! 🎉",
                    description=f"Congratulations! You successfully achieved your target of ₹{float(goal.target_amount):,.2f}.",
                    category="Goals"
                )

                # 2. Notification
                try:
                    from notifications.services.event_service import EventService
                    EventService.publish_event(
                        user=user,
                        event_type="goal_completed",
                        title="Goal Completed 🏆",
                        message=f"Congratulations! You completed your {goal.goal_name} Goal.",
                        category="Goals",
                        priority="High",
                        notification_type="Achievement",
                        action_url="/profile/"
                    )
                except Exception:
                    pass

                # 3. Unlock Achievement
                try:
                    from achievements.services import AchievementService
                    AchievementService.check_and_unlock(user, "Goal Achiever")
                except Exception:
                    pass

                # 4. Generate Explainable AI Summary
                try:
                    from user_profile.services.explainability_service import ExplainabilityService
                    ExplainabilityService.generate_goal_completion_summary(user, goal)
                except Exception:
                    pass

    @staticmethod
    def seed_default_goals(user):
        if not user or not user.is_authenticated:
            return
        if FinancialGoal.objects.filter(user=user, is_deleted=False).exists():
            return

        # Create realistic default goals
        from datetime import timedelta
        now = timezone.now().date()
        
        g1 = FinancialGoal.objects.create(
            user=user,
            goal_name="Emergency Fund",
            goal_type="Emergency Fund",
            target_amount=150000.00,
            current_progress=90000.00,
            monthly_contribution=10000.00,
            deadline=now + timedelta(days=180),
            priority="High",
            status="Active",
            is_primary=True,
            completion_percentage=60.0
        )
        GoalContribution.objects.create(goal=g1, amount=30000.00, notes="Initial seed savings")
        GoalContribution.objects.create(goal=g1, amount=10000.00, notes="Monthly deposit")

        g2 = FinancialGoal.objects.create(
            user=user,
            goal_name="Buy House Downpayment",
            goal_type="Buy House",
            target_amount=1500000.00,
            current_progress=350000.00,
            monthly_contribution=25000.00,
            deadline=now + timedelta(days=1095),
            priority="High",
            status="Active",
            is_primary=False,
            completion_percentage=23.33
        )

        g3 = FinancialGoal.objects.create(
            user=user,
            goal_name="Dream Vacation to Japan",
            goal_type="Vacation",
            target_amount=200000.00,
            current_progress=200000.00,
            monthly_contribution=15000.00,
            deadline=now - timedelta(days=30),
            priority="Medium",
            status="Completed",
            is_primary=False,
            completion_percentage=100.0
        )
