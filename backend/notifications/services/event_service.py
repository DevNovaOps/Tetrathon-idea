from notifications.services.notification_service import NotificationService

class EventService:
    @staticmethod
    def publish_event(user, event_type, title, message, category='General', priority='Medium', notification_type='Information', action_url=None, action_label=None, metadata=None):
        if not user or not user.is_authenticated:
            return None
        if metadata is None:
            metadata = {}
        metadata['event_type'] = event_type
        return NotificationService.create_notification(
            user=user,
            title=title,
            message=message,
            category=category,
            priority=priority,
            notification_type=notification_type,
            action_url=action_url,
            action_label=action_label,
            metadata=metadata
        )

    @staticmethod
    def notify_income_added(user, amount, source="Income"):
        return EventService.publish_event(
            user=user,
            event_type="income_added",
            title="Income Added",
            message=f"New income transaction of ₹{amount} added under {source}.",
            category="Dashboard",
            priority="Medium",
            notification_type="Success",
            action_url="/dashboard/"
        )

    @staticmethod
    def notify_expense_added(user, amount, category_name="General"):
        return EventService.publish_event(
            user=user,
            event_type="expense_added",
            title="Expense Added",
            message=f"New expense of ₹{amount} logged in {category_name}.",
            category="Dashboard",
            priority="Medium",
            notification_type="Information",
            action_url="/dashboard/"
        )

    @staticmethod
    def notify_lesson_completed(user, lesson_title, xp):
        return EventService.publish_event(
            user=user,
            event_type="lesson_completed",
            title="Lesson Completed",
            message=f"You completed '{lesson_title}' and earned +{xp} XP!",
            category="Learning",
            priority="Low",
            notification_type="Education",
            action_url="/learn/"
        )

    @staticmethod
    def notify_course_completed(user, course_title):
        return EventService.publish_event(
            user=user,
            event_type="course_completed",
            title="Course Mastered! 🎓",
            message=f"Congratulations on completing 100% of '{course_title}'.",
            category="Learning",
            priority="High",
            notification_type="Achievement",
            action_url="/learn/"
        )

    @staticmethod
    def notify_badge_unlocked(user, badge_title, xp):
        return EventService.publish_event(
            user=user,
            event_type="badge_unlocked",
            title=f"New Badge Unlocked: {badge_title} 🏅",
            message=f"You've unlocked the '{badge_title}' achievement and earned +{xp} XP!",
            category="Achievements",
            priority="High",
            notification_type="Achievement",
            action_url="/achievements/"
        )

    @staticmethod
    def notify_ai_recommendation(user, recommendation_text, reason="AI Assessment"):
        return EventService.publish_event(
            user=user,
            event_type="ai_recommendation",
            title="AI Recommendation 🧠",
            message=recommendation_text,
            category="AI Insights",
            priority="High",
            notification_type="AI Recommendation",
            action_url="/ai-assistant/",
            metadata={"reason": reason}
        )

    @staticmethod
    def notify_simulation_completed(user, projection_year, projected_amount):
        return EventService.publish_event(
            user=user,
            event_type="simulation_completed",
            title="Growth Simulation Completed 📈",
            message=f"Your wealth projection for {projection_year} is estimated at ₹{projected_amount:,.2f}.",
            category="Simulator",
            priority="Medium",
            notification_type="Information",
            action_url="/simulator/"
        )

    @staticmethod
    def notify_report_generated(user, report_type="Monthly"):
        return EventService.publish_event(
            user=user,
            event_type="report_generated",
            title=f"{report_type} Report Ready 📄",
            message=f"Your {report_type.lower()} financial report is ready for review and download.",
            category="Reports",
            priority="Medium",
            notification_type="Information",
            action_url="/reports/"
        )

    @staticmethod
    def notify_profile_updated(user):
        return EventService.publish_event(
            user=user,
            event_type="profile_updated",
            title="Profile Updated Successfully 👤",
            message="Your contact details and preferences have been updated.",
            category="Profile",
            priority="Low",
            notification_type="Information",
            action_url="/profile/"
        )
