from rest_framework import serializers
from .models import ImprovementPlan, ImprovementTask, WeeklyRoadmap

class ImprovementTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImprovementTask
        fields = ['id', 'title', 'description', 'priority', 'expected_points', 'difficulty', 'duration', 'status', 'order']

class WeeklyRoadmapSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyRoadmap
        fields = ['id', 'week_number', 'title', 'description', 'status']

class ImprovementPlanSerializer(serializers.ModelSerializer):
    tasks = ImprovementTaskSerializer(many=True, read_only=True)
    roadmap_weeks = WeeklyRoadmapSerializer(many=True, read_only=True)
    completed_tasks = serializers.SerializerMethodField()
    total_tasks = serializers.SerializerMethodField()

    class Meta:
        model = ImprovementPlan
        fields = [
            'id', 'current_score', 'estimated_score', 'target_score', 
            'completion_percentage', 'estimated_days', 'tasks', 'roadmap_weeks',
            'completed_tasks', 'total_tasks'
        ]

    def get_completed_tasks(self, obj):
        return obj.tasks.filter(status='Completed').count()

    def get_total_tasks(self, obj):
        return obj.tasks.count()
