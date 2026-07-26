from achievements.models import UserLevel

class RewardService:
    @staticmethod
    def award_xp(user, amount, reason="General Learning"):
        if not user or not user.is_authenticated:
            return None
        
        level_obj, _ = UserLevel.objects.get_or_create(user=user)
        level_obj.xp += amount
        leveled_up = level_obj.update_level()
        level_obj.save()
        
        return {
            "new_xp": level_obj.xp,
            "current_level": level_obj.current_level,
            "leveled_up": leveled_up,
            "xp_awarded": amount,
            "reason": reason
        }

    @staticmethod
    def get_user_level(user):
        if not user or not user.is_authenticated:
            return {
                "xp": 0,
                "current_level": "Beginner",
                "longest_streak": 0,
                "current_streak": 0
            }
        level_obj, _ = UserLevel.objects.get_or_create(user=user)
        level_obj.update_level()
        level_obj.save()
        return {
            "xp": level_obj.xp,
            "current_level": level_obj.current_level,
            "longest_streak": level_obj.longest_streak,
            "current_streak": level_obj.current_streak
        }
