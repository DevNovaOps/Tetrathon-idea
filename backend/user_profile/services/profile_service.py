from user_profile.models import UserProfile, FinancialGoal, ConnectedBank, ConnectedUPI, ConnectedCard

class ProfileService:
    @staticmethod
    def get_profile(user):
        if not user or not user.is_authenticated:
            return None
        profile, created = UserProfile.objects.get_or_create(user=user)
        if created or not profile.email:
            profile.email = user.email
            profile.full_name = user.full_name or ""
            profile.phone = user.phone or ""
            profile.country = user.country or "India"
            profile.save()
        
        # Calculate completion percentage dynamically
        comp = ProfileService.calculate_completion(profile)
        if profile.completion_percentage != comp:
            profile.completion_percentage = comp
            profile.save()
        return profile

    @staticmethod
    def update_profile(user, data):
        if not user or not user.is_authenticated:
            return {"error": "Authentication required"}
        profile = ProfileService.get_profile(user)
        
        fields = [
            'full_name', 'profile_picture', 'phone', 'email', 'date_of_birth',
            'gender', 'occupation', 'education', 'address', 'city', 'state',
            'country', 'preferred_language', 'preferred_currency', 'time_zone'
        ]
        for f in fields:
            if f in data:
                val = data[f]
                if val is not None:
                    setattr(profile, f, val)
                    
        # Synchronize with base user model if name or phone changed
        if 'full_name' in data and data['full_name']:
            user.full_name = data['full_name']
            user.save()
        if 'phone' in data and data['phone']:
            user.phone = data['phone']
            user.save()

        comp = ProfileService.calculate_completion(profile)
        profile.completion_percentage = comp
        profile.save()
        
        # Record timeline event
        from user_profile.services.timeline_service import TimelineService
        TimelineService.record_event(
            user=user,
            event_type="profile_updated",
            title="Profile Updated Successfully",
            description="Your personal details and preferences have been updated.",
            category="Profile"
        )
        return profile

    @staticmethod
    def calculate_completion(profile):
        if not profile or not profile.user:
            return 0
        user = profile.user
        score = 0
        total_checks = 9
        
        # 1. Name
        if profile.full_name or user.full_name:
            score += 1
        # 2. Phone
        if profile.phone or user.phone:
            score += 1
        # 3. Email
        if profile.email or user.email:
            score += 1
        # 4. Occupation
        if profile.occupation:
            score += 1
        # 5. DOB
        if profile.date_of_birth:
            score += 1
        # 6. Goals (at least 1 active goal)
        if FinancialGoal.objects.filter(user=user, is_deleted=False, status='Active').exists():
            score += 1
        # 7. Bank Connected
        if ConnectedBank.objects.filter(user=user, is_deleted=False).exists() or \
           ConnectedUPI.objects.filter(user=user, is_deleted=False).exists() or \
           ConnectedCard.objects.filter(user=user, is_deleted=False).exists():
            score += 1
        # 8. Risk Assessment
        try:
            from risk_profile.models import UserRiskProfile
            if UserRiskProfile.objects.filter(user=user).exists() or user.onboarding_completed:
                score += 1
        except ImportError:
            if user.onboarding_completed:
                score += 1
        # 9. Learning Started
        try:
            from learning.models import UserProgress
            if UserProgress.objects.filter(user=user).exists():
                score += 1
        except ImportError:
            score += 1
            
        percentage = int((score / total_checks) * 100)
        return min(percentage, 100)
