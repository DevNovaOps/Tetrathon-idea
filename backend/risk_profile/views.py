from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .orchestrator import RiskProfileOrchestrator
from .models import RiskProfile
from .serializers import RiskProfileSerializer

class RiskProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieves the latest Risk Profile. 
        Forces a recalculation if the profile doesn't exist yet, acting as a fallback
        if signals haven't fired.
        """
        try:
            profile = RiskProfile.objects.get(user=request.user)
        except RiskProfile.DoesNotExist:
            profile = RiskProfileOrchestrator.run_pipeline(request.user)
            if not profile:
                return Response({"success": False, "error": "Incomplete profile."}, status=400)
                
        serializer = RiskProfileSerializer(profile)
        return Response({
            "success": True,
            "data": serializer.data
        })
