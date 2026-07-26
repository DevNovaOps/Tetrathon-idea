"""
Cascade signals for Transaction module.
Transaction create → update snapshot, credit score, risk profile, notifications, AI memory.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Transaction


@receiver(post_save, sender=Transaction)
def cascade_on_transaction_create(sender, instance, created, **kwargs):
    """When a new transaction is created, cascade updates across modules."""
    if not created:
        return

    user = instance.user

    # 1. Update Financial Snapshot
    try:
        from user_profile.services.snapshot_service import SnapshotService
        SnapshotService.record_snapshot(user)
    except Exception:
        pass

    # 2. Notification for large transactions
    try:
        amount = float(instance.amount)
        if amount >= 5000 and not instance.is_income:
            from notifications.services.event_service import EventService
            EventService.publish_event(
                user=user,
                event_type="large_expense",
                title="Large Expense Detected 💸",
                message=f"₹{amount:,.0f} spent at {instance.merchant or instance.category}.",
                category="Dashboard",
                priority="Medium",
                notification_type="Warning",
                action_url="/dashboard/"
            )
        elif instance.is_income and amount >= 10000:
            from notifications.services.event_service import EventService
            EventService.publish_event(
                user=user,
                event_type="income_received",
                title="Income Received 🎉",
                message=f"₹{amount:,.0f} credited from {instance.merchant or 'income source'}.",
                category="Dashboard",
                priority="Low",
                notification_type="Success",
                action_url="/dashboard/"
            )
    except Exception:
        pass

    # 3. Record AI Memory
    try:
        from ai_memory.memory_service import MemoryService
        direction = "Income" if instance.is_income else "Expense"
        MemoryService.record_memory(
            user=user,
            memory_type='transaction_pattern',
            title=f'{direction}: {instance.merchant or instance.category}',
            summary=f"₹{float(instance.amount):,.0f} via {instance.payment_method} on {instance.date}.",
            data={
                'amount': float(instance.amount),
                'category': instance.category,
                'is_income': instance.is_income,
                'merchant': instance.merchant,
                'payment_method': instance.payment_method,
            }
        )
    except Exception:
        pass
