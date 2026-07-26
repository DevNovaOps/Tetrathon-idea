from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .simulation_service import SimulationService

class SimulationProjectView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        sip = request.GET.get('sip')
        years = request.GET.get('years')
        scenario = request.GET.get('scenario')
        goal_id = request.GET.get('goal_id')
        
        result = SimulationService.run_simulation(request.user, sip, years, scenario, goal_id)
        try:
            from achievements.services.unlock_service import UnlockService
            UnlockService.check_and_unlock(request.user, 'simulator_run', 1)
        except Exception:
            pass
        return Response(result)
