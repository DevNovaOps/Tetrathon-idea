from django.utils import timezone
from user_profile.models import FinancialSnapshotHistory

class SnapshotService:
    @staticmethod
    def get_financial_snapshot(user):
        if not user or not user.is_authenticated:
            return {
                "credit_score": 730,
                "risk_profile": "Moderately Aggressive",
                "monthly_income": 65000.00,
                "monthly_savings": 18500.00,
                "investment_portfolio": 240000.00,
                "net_worth": 420000.00,
                "financial_health_score": 86
            }

        # 1. Credit Score
        c_score = 730
        try:
            from credit_score.models import UserCreditScore
            cs = UserCreditScore.objects.filter(user=user).order_by('-updated_at').first()
            if cs and cs.score:
                c_score = cs.score
        except Exception:
            pass

        # 2. Risk Profile
        r_profile = "Moderately Aggressive"
        try:
            from risk_profile.models import UserRiskProfile
            rp = UserRiskProfile.objects.filter(user=user).order_by('-updated_at').first()
            if rp and rp.risk_category:
                r_profile = rp.risk_category
        except Exception:
            pass

        # 3. Income & Savings from Dashboard / Onboarding
        m_income = 65000.00
        m_savings = 18500.00
        try:
            from dashboard.services import DashboardService
            summary = DashboardService.get_user_summary(user)
            if summary:
                if summary.get('total_income'):
                    m_income = float(summary['total_income'])
                if summary.get('total_savings') or summary.get('net_savings'):
                    m_savings = float(summary.get('total_savings') or summary.get('net_savings'))
        except Exception:
            try:
                from onboarding.models import UserFinancialProfile
                ufp = UserFinancialProfile.objects.filter(user=user).first()
                if ufp:
                    if ufp.monthly_income:
                        m_income = float(ufp.monthly_income)
                    if ufp.monthly_savings:
                        m_savings = float(ufp.monthly_savings)
            except Exception:
                pass

        # 4. Investment Portfolio
        inv_portfolio = 240000.00
        try:
            from investment.models import Portfolio
            port = Portfolio.objects.filter(user=user).first()
            if port and port.total_value:
                inv_portfolio = float(port.total_value)
        except Exception:
            pass

        # 5. Net Worth & Health Score
        n_worth = float(inv_portfolio) + (float(m_savings) * 6)
        if n_worth == 0:
            n_worth = 420000.00

        health_score = 86
        if m_income > 0:
            savings_rate = (m_savings / m_income) * 100
            health_score = int(min(50 + (savings_rate * 1.2) + ((c_score - 600) * 0.1), 99))

        snapshot_data = {
            "credit_score": c_score,
            "risk_profile": r_profile,
            "monthly_income": round(m_income, 2),
            "monthly_savings": round(m_savings, 2),
            "investment_portfolio": round(inv_portfolio, 2),
            "net_worth": round(n_worth, 2),
            "financial_health_score": health_score
        }

        # Automatically record to memory (FinancialSnapshotHistory) if none recorded today
        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        if not FinancialSnapshotHistory.objects.filter(user=user, recorded_at__gte=today_start).exists():
            FinancialSnapshotHistory.objects.create(
                user=user,
                credit_score=c_score,
                risk_profile=r_profile,
                monthly_income=m_income,
                monthly_savings=m_savings,
                investment_portfolio=inv_portfolio,
                net_worth=n_worth,
                financial_health_score=health_score
            )

        return snapshot_data
