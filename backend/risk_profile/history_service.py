from .models import RiskHistory, RiskProfile

class HistoryService:
    """
    Manages the immutable audit log of risk assessments.
    """
    
    @staticmethod
    def log_history_if_changed(user, current_score: int, current_bucket: str):
        """
        Creates a new RiskHistory record only if the score or bucket has changed
        since the last assessment, preventing duplicate identical entries.
        """
        last_history = RiskHistory.objects.filter(user=user).order_by('-assessment_timestamp').first()
        
        previous_score = None
        previous_bucket = ""
        
        if last_history:
            if last_history.current_score == current_score and last_history.current_bucket == current_bucket:
                return # No change, don't bloat the history log
                
            previous_score = last_history.current_score
            previous_bucket = last_history.current_bucket
            
        RiskHistory.objects.create(
            user=user,
            previous_score=previous_score,
            current_score=current_score,
            previous_bucket=previous_bucket,
            current_bucket=current_bucket
        )
