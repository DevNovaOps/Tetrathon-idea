from django.utils import timezone
from user_profile.models import UserTimeline

class TimelineService:
    @staticmethod
    def get_timeline(user, limit=30):
        if not user or not user.is_authenticated:
            return UserTimeline.objects.none()
        return UserTimeline.objects.filter(user=user).order_by('-created_at')[:limit]

    @staticmethod
    def record_event(user, event_type, title, description="", category="General", metadata=None):
        if not user or not user.is_authenticated:
            return None
        if metadata is None:
            metadata = {}
        return UserTimeline.objects.create(
            user=user,
            event_type=event_type,
            title=title,
            description=description,
            category=category,
            metadata=metadata
        )

    @staticmethod
    def seed_default_timeline(user):
        if not user or not user.is_authenticated:
            return
        if UserTimeline.objects.filter(user=user).exists():
            return

        from datetime import timedelta
        now = timezone.now()
        
        defaults = [
            {
                "type": "ai_recommendation_accepted",
                "title": "AI Recommendation Accepted",
                "desc": "Applied SIP step-up strategy recommended by Finora AI Assistant.",
                "cat": "AI Insights",
                "hours": 2
            },
            {
                "type": "credit_improved",
                "title": "Credit Score Improved (+18 pts)",
                "desc": "Your credit score reached 730 following timely credit card bill settlements.",
                "cat": "Credit Score",
                "hours": 14
            },
            {
                "type": "lesson_completed",
                "title": "Lesson Completed: Master Emergency Funds",
                "desc": "Earned +100 XP and unlocked the Emergency Planner badge.",
                "cat": "Learning",
                "hours": 36
            },
            {
                "type": "simulator_used",
                "title": "Growth Simulation Completed",
                "desc": "Projected retirement corpus of ₹2.4 Cr at age 55 with 12% CAGR.",
                "cat": "Simulator",
                "hours": 48
            },
            {
                "type": "goal_created",
                "title": "New Goal Created: Buy House Downpayment",
                "desc": "Target set for ₹15,00,000 over 3 years with monthly deposit of ₹25,000.",
                "cat": "Goals",
                "hours": 72
            },
            {
                "type": "report_downloaded",
                "title": "Monthly Report Downloaded",
                "desc": "Downloaded comprehensive financial health PDF report for June.",
                "cat": "Reports",
                "hours": 120
            },
            {
                "type": "investment_started",
                "title": "New SIP Investment Started",
                "desc": "Initiated monthly SIP of ₹5,000 in Nifty 50 Index Fund.",
                "cat": "Investments",
                "hours": 168
            },
            {
                "type": "profile_updated",
                "title": "Profile Verified & Onboarding Completed",
                "desc": "Connected primary HDFC Bank account and completed risk assessment.",
                "cat": "Profile",
                "hours": 240
            }
        ]

        for d in defaults:
            dt = now - timedelta(hours=d["hours"])
            evt = UserTimeline.objects.create(
                user=user,
                event_type=d["type"],
                title=d["title"],
                description=d["desc"],
                category=d["cat"]
            )
            UserTimeline.objects.filter(id=evt.id).update(created_at=dt)
