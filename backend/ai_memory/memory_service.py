"""
AI Memory Service — record, query, and aggregate memory for Explainable AI.
"""
from datetime import timedelta
from django.utils import timezone
from django.db.models import Count

from .models import MemoryEntry


class MemoryService:

    @staticmethod
    def record_memory(user, memory_type: str, title: str, summary: str, data: dict = None):
        """Record a new memory entry. Called by signals and services across all modules."""
        if not user or not hasattr(user, 'is_authenticated') or not user.is_authenticated:
            return None
        return MemoryEntry.objects.create(
            user=user,
            memory_type=memory_type,
            title=title,
            summary=summary,
            data=data or {},
        )

    @staticmethod
    def get_memories(user, memory_type: str = None, limit: int = 50) -> list:
        """Retrieve memories, optionally filtered by type."""
        qs = MemoryEntry.objects.filter(user=user)
        if memory_type:
            qs = qs.filter(memory_type=memory_type)
        return list(qs[:limit].values('id', 'memory_type', 'title', 'summary', 'data', 'created_at'))

    @staticmethod
    def get_memory_context(user) -> dict:
        """
        Aggregated memory context for Explainable AI.
        Returns structured data covering all memory dimensions.
        """
        if not user or not hasattr(user, 'is_authenticated') or not user.is_authenticated:
            return {"memories": [], "summary": {}}

        qs = MemoryEntry.objects.filter(user=user)

        # Count by type
        type_counts = dict(
            qs.values_list('memory_type')
            .annotate(count=Count('id'))
            .values_list('memory_type', 'count')
        )

        # Recent memories (last 30 days)
        recent_cutoff = timezone.now() - timedelta(days=30)
        recent = list(
            qs.filter(created_at__gte=recent_cutoff)
            .values('memory_type', 'title', 'summary', 'created_at')[:20]
        )
        for m in recent:
            m['created_at'] = m['created_at'].isoformat()

        # Key highlights
        latest_risk = qs.filter(memory_type='risk_change').first()
        latest_credit = qs.filter(memory_type='credit_change').first()
        latest_goal = qs.filter(memory_type__in=['goal_progress', 'goal_completed']).first()
        latest_learning = qs.filter(memory_type='learning_milestone').first()

        return {
            "type_counts": type_counts,
            "total_memories": qs.count(),
            "recent_memories": recent,
            "highlights": {
                "latest_risk": {
                    "title": latest_risk.title if latest_risk else None,
                    "summary": latest_risk.summary if latest_risk else None,
                } if latest_risk else None,
                "latest_credit": {
                    "title": latest_credit.title if latest_credit else None,
                    "summary": latest_credit.summary if latest_credit else None,
                } if latest_credit else None,
                "latest_goal": {
                    "title": latest_goal.title if latest_goal else None,
                    "summary": latest_goal.summary if latest_goal else None,
                } if latest_goal else None,
                "latest_learning": {
                    "title": latest_learning.title if latest_learning else None,
                    "summary": latest_learning.summary if latest_learning else None,
                } if latest_learning else None,
            }
        }

    @staticmethod
    def get_improvement_trends(user) -> list:
        """
        Produce natural-language improvement insights from memory data.
        Example: 'You have improved your savings rate by 18% over the last four months.'
        Never hallucinate — only use stored memory entries.
        """
        trends = []
        qs = MemoryEntry.objects.filter(user=user)

        # Credit score changes
        credit_entries = list(
            qs.filter(memory_type='credit_change').order_by('created_at')[:10]
        )
        if len(credit_entries) >= 2:
            first_data = credit_entries[0].data or {}
            last_data = credit_entries[-1].data or {}
            old_score = first_data.get('credit_score', 0)
            new_score = last_data.get('credit_score', 0)
            if old_score > 0 and new_score > old_score:
                diff = new_score - old_score
                trends.append(
                    f"Your credit score has improved by +{diff} points from {old_score} to {new_score} "
                    f"since {credit_entries[0].created_at.strftime('%B %Y')}."
                )

        # Goals completed
        completed_goals = qs.filter(memory_type='goal_completed').count()
        if completed_goals > 0:
            trends.append(
                f"You have successfully completed {completed_goals} financial goal{'s' if completed_goals > 1 else ''}."
            )

        # Risk changes
        risk_entries = list(
            qs.filter(memory_type='risk_change').order_by('created_at')[:10]
        )
        if len(risk_entries) >= 2:
            old_bucket = (risk_entries[0].data or {}).get('risk_bucket', '')
            new_bucket = (risk_entries[-1].data or {}).get('risk_bucket', '')
            if old_bucket and new_bucket and old_bucket != new_bucket:
                trends.append(
                    f"Your risk profile has shifted from {old_bucket} to {new_bucket}."
                )

        # Learning milestones
        learning_count = qs.filter(memory_type='learning_milestone').count()
        if learning_count > 0:
            trends.append(
                f"You have achieved {learning_count} learning milestone{'s' if learning_count > 1 else ''}."
            )

        # Transaction patterns
        tx_count = qs.filter(memory_type='transaction_pattern').count()
        if tx_count > 0:
            trends.append(
                f"{tx_count} transactions have been tracked and analyzed for spending insights."
            )

        if not trends:
            trends.append(
                "Start adding transactions, goals, and completing assessments to build your financial memory."
            )

        return trends
