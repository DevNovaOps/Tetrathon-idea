from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .services import ImproveScoreService
from .serializers import ImprovementPlanSerializer
from .metrics import ImprovementMetricsGenerator

class ImproveScoreAPIView(APIView):
    """GET /api/improve-score/"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            plan = ImproveScoreService.get_or_generate_plan(request.user)
            serializer = ImprovementPlanSerializer(plan)
            
            # Generate success metrics dynamically
            # Assuming potential expected_points is the difference between target and current score
            expected_points = plan.target_score - plan.current_score
            metrics = ImprovementMetricsGenerator(request.user.profile, expected_points).generate()
            
            data = serializer.data
            data['metrics'] = metrics
            
            return Response({
                "success": True,
                "data": data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "success": False,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class ImproveScoreProgressAPIView(APIView):
    """GET /api/improve-score/progress/"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            plan = ImproveScoreService.get_or_generate_plan(request.user)
            serializer = ImprovementPlanSerializer(plan)
            
            return Response({
                "success": True,
                "data": {
                    "completed_tasks": serializer.data['completed_tasks'],
                    "total_tasks": serializer.data['total_tasks'],
                    "completion_percentage": serializer.data['completion_percentage']
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CompleteTaskAPIView(APIView):
    """POST /api/improve-score/task/<uuid>/complete/"""
    permission_classes = [IsAuthenticated]

    def post(self, request, task_id):
        try:
            plan = ImproveScoreService.complete_task(task_id, request.user)
            serializer = ImprovementPlanSerializer(plan)
            return Response({
                "success": True,
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class RegeneratePlanAPIView(APIView):
    """POST /api/improve-score/regenerate/"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            plan = ImproveScoreService.generate_new_plan(request.user)
            serializer = ImprovementPlanSerializer(plan)
            
            expected_points = plan.target_score - plan.current_score
            metrics = ImprovementMetricsGenerator(request.user.profile, expected_points).generate()
            
            data = serializer.data
            data['metrics'] = metrics
            
            return Response({
                "success": True,
                "data": data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
