from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .orchestrator import InvestmentOrchestrator
from .serializers import InvestmentProfileSerializer
from config.disclaimers import EDUCATIONAL_DISCLAIMER

class InvestmentPlanView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Generate or retrieve the investment plan
        # The orchestrator handles consuming the snapshot and updating the profile
        profile = InvestmentOrchestrator.run_pipeline(request.user)
        
        serializer = InvestmentProfileSerializer(profile)
        data = serializer.data
        data['educational_disclaimer'] = EDUCATIONAL_DISCLAIMER
        return Response(data)

