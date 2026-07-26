from notifications.services.preference_service import PreferenceService
from notifications.services.history_service import HistoryService

class DeliveryService:
    @staticmethod
    def deliver(notification):
        if not notification:
            return False
        # Check preferences
        enabled = PreferenceService.is_category_enabled(notification.user, notification.category)
        if not enabled:
            # If user disabled this category, we still keep it in DB but maybe mark dismissed or skip history
            return False
        
        # Log to history
        HistoryService.record_delivery(notification)
        return True
