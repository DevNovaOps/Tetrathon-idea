"""Dashboard Analytics Service and AI Insights."""
import datetime
from decimal import Decimal

from django.utils import timezone
from onboarding.models import UserProfile
from .constants import DEFAULT_EXPENSE_DISTRIBUTION


class DashboardAnalyticsService:
    """Service to compute dashboard metrics, charts, and insights."""

    def __init__(self, user, profile: UserProfile):
        self.user = user
        self.profile = profile

    def _format_currency(self, value) -> str:
        if value is None:
            return "₹0"
        return f"₹{int(value):,}"

    def get_dashboard_data(self) -> dict:
        """Aggregate all data required for the frontend."""
        return {
            "user": self._get_user_info(),
            "profile": self._get_profile_info(),
            "financial_summary": self._get_financial_summary(),
            "analytics": self._get_analytics(),
            "charts": self._get_charts_data(),
            "insights": self._generate_insights(),
            "activities": self._get_recent_activity(),
            "quick_actions": self._get_quick_actions(),
        }

    def _get_user_info(self) -> dict:
        return {
            "full_name": self.user.full_name or self.user.email.split('@')[0],
            "email": self.user.email,
            "avatar": self.user.profile_picture,
            "initials": (self.user.full_name[0].upper() if self.user.full_name else self.user.email[0].upper()),
            "last_login": self.user.last_activity.isoformat() if self.user.last_activity else None,
            "member_since": self.user.date_joined.strftime("%B %Y"),
        }

    def _get_profile_info(self) -> dict:
        return {
            "country": self.user.country or "India",
            "completion": self._calculate_profile_completion(),
        }

    def _get_financial_summary(self) -> dict:
        return {
            "monthly_income": self._format_currency(self.profile.monthly_income),
            "monthly_expenses": self._format_currency(self.profile.monthly_expenses),
            "savings": self._format_currency(self.profile.savings),
            "investment_budget": self._format_currency(self.profile.monthly_investment_budget),
            "emergency_fund": self.profile.emergency_fund or "Not Set",
            "risk_preference": self.profile.risk_preference or "Not Set",
            "investment_experience": self.profile.investment_experience or "None",
            "financial_goal": self.profile.financial_goal or "Not Set",
            "investment_duration": self.profile.investment_duration or "Not Set",
        }

    def _calculate_profile_completion(self) -> int:
        score = 25  # User exists
        if self.profile.step1_completed:
            score += 25
        if self.profile.step2_completed:
            score += 25
        if self.profile.step3_completed:
            score += 25
        return score

    def _get_analytics(self) -> dict:
        income = self.profile.monthly_income or Decimal(0)
        expenses = self.profile.monthly_expenses or Decimal(0)
        savings = self.profile.savings or Decimal(0)
        cash_flow = income - expenses

        savings_rate = round((cash_flow / income) * 100) if income > 0 else 0
        expense_ratio = round((expenses / income) * 100) if income > 0 else 0

        # Health score simple heuristic
        health_score = 50
        if savings_rate >= 20: health_score += 20
        if self.profile.emergency_fund and "Yes" in self.profile.emergency_fund: health_score += 15
        if self.profile.monthly_investment_budget and self.profile.monthly_investment_budget > 0: health_score += 15

        # Readiness
        readiness = 40
        if health_score > 70: readiness += 40
        if self.profile.investment_experience and "Intermediate" in self.profile.investment_experience: readiness += 20

        return {
            "savings_rate": savings_rate,
            "expense_ratio": expense_ratio,
            "monthly_cash_flow": self._format_currency(cash_flow),
            "financial_health_score": min(health_score, 100),
            "profile_completion": self._calculate_profile_completion(),
            "investment_readiness_score": min(readiness, 100),
            "goal_progress": 45,  # Dummy value for UI
        }

    def _get_charts_data(self) -> dict:
        income = self.profile.monthly_income or Decimal(0)
        expenses = self.profile.monthly_expenses or Decimal(0)
        
        # 1. Income vs Expense (Dummy historical data for 7 months, ending in current month)
        now = timezone.now()
        months = []
        for i in range(6, -1, -1):
            d = now - datetime.timedelta(days=30 * i)
            months.append(d.strftime('%b'))
            
        # Create slight variations for historical data based on current income/expense
        income_data = [float(income) * (0.9 + (i * 0.02)) for i in range(7)]
        expense_data = [float(expenses) * (0.85 + (i * 0.03)) for i in range(7)]

        income_expense_chart = {
            "labels": months,
            "datasets": [
                {
                    "label": "Income",
                    "data": income_data,
                    "backgroundColor": "#3B82F6",
                },
                {
                    "label": "Expense",
                    "data": expense_data,
                    "backgroundColor": "#A855F7",
                }
            ]
        }

        # 2. Spending Categories Donut Chart
        # Use configurable distribution from constants
        categories = list(DEFAULT_EXPENSE_DISTRIBUTION.keys())
        percentages = list(DEFAULT_EXPENSE_DISTRIBUTION.values())
        
        donut_data = {
            "labels": categories,
            "datasets": [{
                "data": [int(p * 100) for p in percentages],
                "backgroundColor": ["#3B82F6", "#F97316", "#10B981", "#A855F7", "#06B6D4"],
            }],
            "total_spent": self._format_currency(expenses)
        }

        return {
            "income_vs_expense": income_expense_chart,
            "spending_categories": donut_data,
        }

    def _generate_insights(self) -> list:
        insights = []
        
        # Rule 1: Savings Rate
        income = self.profile.monthly_income or Decimal(0)
        expenses = self.profile.monthly_expenses or Decimal(0)
        cash_flow = income - expenses
        savings_rate = (cash_flow / income) * 100 if income > 0 else 0
        
        if savings_rate > 20:
            insights.append({
                "title": f"Your savings rate is strong at {int(savings_rate)}%.",
                "badge_text": "High Priority",
                "badge_color": "green",
                "icon": "sparkle",
                "desc": "Disciplined spending ensures you're on track to meet your financial goals faster.",
            })
        else:
            insights.append({
                "title": "Boost your savings rate.",
                "badge_text": "Actionable",
                "badge_color": "orange",
                "icon": "alert",
                "desc": f"Your current savings rate is {int(savings_rate)}%. Aiming for 20% will build long-term wealth.",
            })

        # Rule 2: Emergency Fund
        ef = self.profile.emergency_fund or ""
        if "Yes" in ef:
            insights.append({
                "title": "Emergency fund is well-stocked.",
                "badge_text": "Safety Net",
                "badge_color": "cyan",
                "icon": "shield",
                "desc": "Your liquid emergency reserves provide an excellent safety net against unforeseen events.",
            })
        else:
            insights.append({
                "title": "Start building an emergency fund.",
                "badge_text": "Credit Tip",
                "badge_color": "rose",
                "icon": "alert",
                "desc": "Having 3-6 months of expenses saved protects you from unexpected financial shocks.",
            })

        # Rule 3: Risk Profile
        risk = self.profile.risk_preference or ""
        if risk:
            insights.append({
                "title": f"Investment risk remains {risk.split(' ')[0]}.",
                "badge_text": "Portfolio",
                "badge_color": "purple",
                "icon": "trend",
                "desc": f"Your asset allocation should align with a {risk.lower()} strategy for optimal balance.",
            })

        # Rule 4: Bill Payments
        bills = self.profile.bill_payment_habit or ""
        if "On-Time" in bills or "Auto-Debit" in bills:
            insights.append({
                "title": "Maintain timely bill payments.",
                "badge_text": "Credit Tip",
                "badge_color": "emerald",
                "icon": "check",
                "desc": "Consistent on-time payments are the biggest contributor to a high credit score.",
            })
            
        return insights[:6]  # Return max 6 insights

    def _get_recent_activity(self) -> list:
        activities = []
        # Add basic dummy timeline based on user creation
        activities.append({
            "name": "Registration Completed",
            "amount": "",
            "amount_class": "neutral-amt",
            "time": "Just now · Onboarding",
            "icon": "⭐",
        })
        
        if self.profile.onboarding_completed:
            activities.append({
                "name": "Risk Assessment Completed",
                "amount": self.profile.risk_preference or "Unknown",
                "amount_class": "neutral-amt",
                "time": "Recent · AI Neural Evaluation",
                "icon": "🛡️",
            })
            
        if self.profile.monthly_income and self.profile.monthly_income > 0:
            activities.append({
                "name": "Income Profile Set",
                "amount": f"+{self._format_currency(self.profile.monthly_income)}",
                "amount_class": "pos-amt",
                "time": "Recent · Financial Profile",
                "icon": "💼",
            })
            
        return activities

    def _get_quick_actions(self) -> list:
        # Returns static metadata for rendering actions
        return [
            {
                "name": "Improve Credit Score",
                "sub": "View AI Roadmap",
                "icon_bg": "indigo-bg",
                "link": "#credit-score"
            },
            {
                "name": "Start AI Assessment",
                "sub": "Run Neural Check",
                "icon_bg": "emerald-bg",
                "link": "#ai-assistant"
            },
            {
                "name": "View Investment Plan",
                "sub": "Smart Allocation",
                "icon_bg": "purple-bg",
                "link": "#investments"
            },
            {
                "name": "Open Growth Simulator",
                "sub": "Monte Carlo Engine",
                "icon_bg": "cyan-bg",
                "link": "#simulator"
            },
            {
                "name": "Download Report",
                "sub": "Export PDF Summary",
                "icon_bg": "rose-bg",
                "link": "#reports"
            },
            {
                "name": "Learn Finance",
                "sub": "Educational Guides",
                "icon_bg": "amber-bg",
                "link": "#learn"
            },
        ]
