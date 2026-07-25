from django.db import transaction
from onboarding.models import UserProfile
from credit_score.services import CreditScoreService
from .models import ImprovementPlan, ImprovementTask, WeeklyRoadmap
from .generators import TaskGenerator
from .roadmap import RoadmapGenerator
from .constants import STATUS_COMPLETED, STATUS_PENDING, STATUS_IN_PROGRESS, WEEK_STATUS_COMPLETE, WEEK_STATUS_IN_PROGRESS, WEEK_STATUS_UPCOMING

class ImproveScoreService:
    
    @staticmethod
    def get_or_generate_plan(user) -> ImprovementPlan:
        """Fetch existing plan or generate a new one if it doesn't exist."""
        try:
            plan = ImprovementPlan.objects.get(user=user)
            profile = user.profile
            # Sync current score if it drifted
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
        ImprovementPlan.objects.filter(user=user).delete()
        
        profile = getattr(user, 'profile', None)
        if not profile:
            raise ValueError("UserProfile not found.")
            
        current_score = profile.credit_score or 300
        task_data_list = TaskGenerator(profile).generate_tasks()
        total_potential_points = sum(t['expected_points'] for t in task_data_list)
        target_score = min(900, current_score + total_potential_points)
        
        # Initial estimated score (60-day baseline momentum)
        initial_estimated = min(target_score, current_score + int(total_potential_points * 0.15))
        
        plan = ImprovementPlan.objects.create(
            user=user,
            current_score=current_score,
            estimated_score=initial_estimated, 
            target_score=target_score,
            completion_percentage=0.0
        )
        
        tasks_to_create = []
        for task_data in task_data_list:
            tasks_to_create.append(ImprovementTask(
                plan=plan,
                title=task_data['title'],
                description=task_data['description'],
                reason=task_data.get('reason', ''),
                benefit=task_data.get('benefit', ''),
                priority=task_data['priority'],
                expected_points=task_data['expected_points'],
                difficulty=task_data['difficulty'],
                duration=task_data['duration'],
                order=task_data['order']
            ))
        ImprovementTask.objects.bulk_create(tasks_to_create)
        
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
    @transaction.atomic
    def complete_task(task_id: str, user):
        """Marks a task as completed and dynamically updates plan progress and roadmap."""
        try:
            task = ImprovementTask.objects.select_related('plan').get(id=task_id, plan__user=user)
        except ImprovementTask.DoesNotExist:
            raise ValueError("Task not found.")
            
        if task.status == STATUS_COMPLETED:
            return task.plan
            
        task.status = STATUS_COMPLETED
        task.save(update_fields=['status'])
        
        # Synchronize progress and roadmap state
        return ImproveScoreService.recalculate_progress(task.plan)
        
    @staticmethod
    def recalculate_progress(plan: ImprovementPlan) -> ImprovementPlan:
        """Recalculates completion %, estimated score, and cascades roadmap statuses."""
        tasks = plan.tasks.all()
        total_tasks = tasks.count()
        if total_tasks == 0:
            return plan
            
        completed_tasks = [t for t in tasks if t.status == STATUS_COMPLETED]
        in_progress_tasks = [t for t in tasks if t.status == STATUS_IN_PROGRESS]
        completed_count = len(completed_tasks)
        
        # 1. Completion Percentage
        completion_pct = (completed_count / total_tasks) * 100
        
        # 2. Estimated Score (current + 100% of completed points + 30% of in progress points + momentum buffer)
        earned_points = sum(t.expected_points for t in completed_tasks)
        partial_points = sum(t.expected_points * 0.3 for t in in_progress_tasks)
        momentum = 5 if completed_count > 0 else (plan.target_score - plan.current_score) * 0.15
        estimated_score = min(plan.target_score, plan.current_score + earned_points + partial_points + momentum)
        
        plan.completion_percentage = completion_pct
        plan.estimated_score = int(estimated_score)
        plan.save(update_fields=['completion_percentage', 'estimated_score'])
        
        # 3. Synchronize Roadmap Weeks
        # If 1 task is complete, Week 1 is Complete and Week 2 is In Progress, etc.
        roadmaps = list(plan.roadmap_weeks.all().order_by('week_number'))
        for idx, rm in enumerate(roadmaps):
            if idx < completed_count:
                rm.status = WEEK_STATUS_COMPLETE
            elif idx == completed_count:
                rm.status = WEEK_STATUS_IN_PROGRESS
            else:
                rm.status = WEEK_STATUS_UPCOMING
            rm.save(update_fields=['status'])
        
        return plan
