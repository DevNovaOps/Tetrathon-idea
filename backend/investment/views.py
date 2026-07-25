from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .orchestrator import InvestmentOrchestrator
from .serializers import InvestmentProfileSerializer

class InvestmentPlanView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Generate or retrieve the investment plan
        # The orchestrator handles consuming the snapshot and updating the profile
        profile = InvestmentOrchestrator.run_pipeline(request.user)
        
        serializer = InvestmentProfileSerializer(profile)
        return Response(serializer.data)
