from .constants import *

class RoadmapGenerator:
    """Takes generated tasks and spreads them out into a 4-week roadmap."""
    
    def __init__(self, tasks: list):
        self.tasks = tasks

    def generate(self) -> list:
        roadmap = []
        weeks = [
            {"num": 1, "theme": "Bills & Debt", "impacts": ["bills", "debt"]},
            {"num": 2, "theme": "Savings & Budget", "impacts": ["savings", "expenses"]},
            {"num": 3, "theme": "Investments & Security", "impacts": ["investment", "security"]},
            {"num": 4, "theme": "Review & Long-Term", "impacts": ["review", "any"]}
        ]
        
        assigned_tasks = set()
        
        for idx, week in enumerate(weeks):
            # Week 1 starts 'In Progress', others start 'Upcoming'
            initial_status = WEEK_STATUS_IN_PROGRESS if idx == 0 else WEEK_STATUS_UPCOMING
            
            # Try to find a task matching the theme
            task_for_week = None
            for t in self.tasks:
                if t['order'] not in assigned_tasks and (t['impact_type'] in week['impacts'] or "any" in week['impacts']):
                    task_for_week = t
                    break
                    
            if not task_for_week:
                # Just grab the next available highest priority task
                for t in self.tasks:
                    if t['order'] not in assigned_tasks:
                        task_for_week = t
                        break
            
            if task_for_week:
                assigned_tasks.add(task_for_week['order'])
                roadmap.append({
                    "week_number": week["num"],
                    "title": task_for_week['title'],
                    "description": task_for_week['description'],
                    "status": initial_status
                })
            else:
                # Fallback if we don't have 4 tasks
                roadmap.append({
                    "week_number": week["num"],
                    "title": f"{week['theme']} Focus",
                    "description": f"Focus on optimizing your {week['theme'].lower()} this week.",
                    "status": initial_status
                })
                
        return roadmap
