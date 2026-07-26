
"""
Transaction analytics service — spending breakdown, trends, and patterns.
"""
from datetime import date, timedelta
from decimal import Decimal
from django.db.models import Sum, Count, Avg, Q
from django.db.models.functions import TruncMonth

from .models import Transaction


class TransactionAnalyticsService:

    @staticmethod
    def get_spending_summary(user, months: int = 6) -> dict:
        """Category-wise spending breakdown for the last N months."""
        cutoff = date.today() - timedelta(days=30 * months)
        qs = Transaction.objects.filter(
            user=user, is_deleted=False, is_income=False, date__gte=cutoff
        )

        by_category = list(
            qs.values('category')
            .annotate(total=Sum('amount'), count=Count('id'))
            .order_by('-total')
        )

        grand_total = sum(float(c['total'] or 0) for c in by_category)

        breakdown = []
        for c in by_category:
            total = float(c['total'] or 0)
            breakdown.append({
                "category": c['category'],
                "total": total,
                "count": c['count'],
                "percentage": round((total / grand_total * 100), 1) if grand_total > 0 else 0,
            })

        return {
            "total_spending": grand_total,
            "categories": breakdown,
            "period_months": months,
        }

    @staticmethod
    def get_monthly_trend(user, months: int = 6) -> dict:
        """Income vs expense trend over the last N months."""
        cutoff = date.today() - timedelta(days=30 * months)
        qs = Transaction.objects.filter(user=user, is_deleted=False, date__gte=cutoff)

        income_trend = list(
            qs.filter(is_income=True)
            .annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(total=Sum('amount'))
            .order_by('month')
        )

        expense_trend = list(
            qs.filter(is_income=False)
            .annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(total=Sum('amount'))
            .order_by('month')
        )

        return {
            "income": [
                {"month": t['month'].strftime('%b %Y'), "amount": float(t['total'] or 0)}
                for t in income_trend
            ],
            "expenses": [
                {"month": t['month'].strftime('%b %Y'), "amount": float(t['total'] or 0)}
                for t in expense_trend
            ],
        }

    @staticmethod
    def get_transaction_patterns(user) -> dict:
        """Frequency, average amounts, and spending patterns."""
        qs = Transaction.objects.filter(user=user, is_deleted=False)
        total = qs.count()
        if total == 0:
            return {
                "total_transactions": 0,
                "avg_expense": 0,
                "avg_income": 0,
                "most_used_method": "N/A",
                "top_merchant": "N/A",
                "income_count": 0,
                "expense_count": 0,
            }

        expense_qs = qs.filter(is_income=False)
        income_qs = qs.filter(is_income=True)

        avg_expense = expense_qs.aggregate(avg=Avg('amount'))['avg'] or 0
        avg_income = income_qs.aggregate(avg=Avg('amount'))['avg'] or 0

        # Most used payment method
        method_counts = list(
            expense_qs.values('payment_method')
            .annotate(count=Count('id'))
            .order_by('-count')[:1]
        )
        most_used = method_counts[0]['payment_method'] if method_counts else 'upi'

        # Top merchant
        top_merchant_list = list(
            expense_qs.exclude(merchant='')
            .values('merchant')
            .annotate(total=Sum('amount'))
            .order_by('-total')[:1]
        )
        top_merchant = top_merchant_list[0]['merchant'] if top_merchant_list else 'N/A'

        return {
            "total_transactions": total,
            "avg_expense": round(float(avg_expense), 2),
            "avg_income": round(float(avg_income), 2),
            "most_used_method": most_used,
            "top_merchant": top_merchant,
            "income_count": income_qs.count(),
            "expense_count": expense_qs.count(),
        }

    @staticmethod
    def get_full_analytics(user) -> dict:
        """Combined analytics payload for API."""
        return {
            "spending_summary": TransactionAnalyticsService.get_spending_summary(user),
            "monthly_trend": TransactionAnalyticsService.get_monthly_trend(user),
            "patterns": TransactionAnalyticsService.get_transaction_patterns(user),
        }
