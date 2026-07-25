from django.db import transaction
from onboarding.models import UserProfile
from credit_score.services import CreditScoreService
from .models import ImprovementPlan, ImprovementTask, WeeklyRoadmap
from .generators import TaskGenerator
from .roadmap import RoadmapGenerator
from .constants import STATUS_COMPLETED, STATUS_PENDING

class ImproveScoreService:
    
    @staticmethod
    def get_or_generate_plan(user) -> ImprovementPlan:
        """Fetch existing plan or generate a new one if it doesn't exist."""
        try:
            plan = ImprovementPlan.objects.get(user=user)
            # Sync current score just in case it updated
            profile = user.profile
            if plan.current_score != profile.credit_score:
                plan.current_score = profile.credit_score
                plan.save(update_fields=['current_score'])
            return plan
        except ImprovementPlan.DoesNotExist:
            return ImproveScoreService.generate_new_plan(user)

    @staticmethod
    @transaction.atomic
    def generate_new_plan(user) -> ImprovementPlan:
        """Generates a completely new improvement plan."""
        # Cleanup existing if regenerating
        ImprovementPlan.objects.filter(user=user).delete()
        
        # 1. Fetch existing profile and score data
        profile = getattr(user, 'profile', None)
        if not profile:
            raise ValueError("UserProfile not found.")
            
        current_score = profile.credit_score or 300
        
        # 2. Generate tasks dynamically based on metrics
        task_data_list = TaskGenerator(profile).generate_tasks()
        
        # 3. Calculate max potential points
        total_potential_points = sum(t['expected_points'] for t in task_data_list)
        
        # Target score is simply current + total potential (capped at 900)
        target_score = min(900, current_score + total_potential_points)
        
        # 4. Create Plan
        plan = ImprovementPlan.objects.create(
            user=user,
            current_score=current_score,
            estimated_score=current_score,  # Starts at current
            target_score=target_score,
            completion_percentage=0.0
        )
        
        # 5. Create Tasks
        tasks_to_create = []
        for task_data in task_data_list:
            tasks_to_create.append(ImprovementTask(
                plan=plan,
                title=task_data['title'],
                description=task_data['description'],
                priority=task_data['priority'],
                expected_points=task_data['expected_points'],
                difficulty=task_data['difficulty'],
                duration=task_data['duration'],
                order=task_data['order']
            ))
        ImprovementTask.objects.bulk_create(tasks_to_create)
        
        # 6. Generate Roadmap
        roadmap_data_list = RoadmapGenerator(task_data_list).generate()
        roadmap_to_create = []
        for rm in roadmap_data_list:
            roadmap_to_create.append(WeeklyRoadmap(
                plan=plan,
                week_number=rm['week_number'],
                title=rm['title'],
                description=rm['description'],
                status=rm['status']
            ))
        WeeklyRoadmap.objects.bulk_create(roadmap_to_create)
        
        return plan

    @staticmethod
    def complete_task(task_id: str, user):
        """Marks a task as completed and dynamically updates plan progress."""
        try:
            task = ImprovementTask.objects.select_related('plan').get(id=task_id, plan__user=user)
        except ImprovementTask.DoesNotExist:
            raise ValueError("Task not found.")
            
        if task.status == STATUS_COMPLETED:
            return task.plan # Already complete
            
        task.status = STATUS_COMPLETED
        task.save(update_fields=['status'])
        
        return ImproveScoreService.recalculate_progress(task.plan)
        
    @staticmethod
    def recalculate_progress(plan: ImprovementPlan) -> ImprovementPlan:
        """Recalculates completion % and estimated score."""
        tasks = plan.tasks.all()
        total_tasks = tasks.count()
        if total_tasks == 0:
            return plan
            
        completed_tasks = [t for t in tasks if t.status == STATUS_COMPLETED]
        completion_pct = (len(completed_tasks) / total_tasks) * 100
        
        # Estimated score = current + sum(completed task points)
        earned_points = sum(t.expected_points for t in completed_tasks)
        estimated_score = min(900, plan.current_score + earned_points)
        
        plan.completion_percentage = completion_pct
        plan.estimated_score = estimated_score
        plan.save(update_fields=['completion_percentage', 'estimated_score'])
        
        return plan
