import json
import zipfile
import io
from django.http import HttpResponse, JsonResponse
from user_profile.services.profile_service import ProfileService
from user_profile.services.snapshot_service import SnapshotService
from user_profile.services.goal_service import GoalService
from user_profile.services.connected_services_service import ConnectedServicesService
from user_profile.services.timeline_service import TimelineService
from user_profile.services.explainability_service import ExplainabilityService
from user_profile.serializers import (
    UserProfileSerializer, FinancialGoalSerializer, ConnectedBankSerializer,
    ConnectedUPISerializer, ConnectedCardSerializer, UserTimelineSerializer
)

class ExportService:
    @staticmethod
    def get_full_user_data_dict(user):
        if not user or not user.is_authenticated:
            return {}
        profile = ProfileService.get_profile(user)
        snapshot = SnapshotService.get_financial_snapshot(user)
        goals = GoalService.get_goals(user)
        services = ConnectedServicesService.get_services(user)
        timeline = TimelineService.get_timeline(user, limit=100)
        explainability = ExplainabilityService.get_latest_summary(user)
        stats = ExplainabilityService.get_account_statistics(user)

        return {
            "user": {
                "email": user.email,
                "full_name": user.full_name,
                "phone": user.phone,
                "date_joined": user.date_joined.isoformat() if user.date_joined else None
            },
            "profile": UserProfileSerializer(profile).data if profile else {},
            "financial_snapshot": snapshot,
            "goals": FinancialGoalSerializer(goals, many=True).data,
            "connected_services": {
                "banks": ConnectedBankSerializer(services["banks"], many=True).data,
                "upis": ConnectedUPISerializer(services["upis"], many=True).data,
                "cards": ConnectedCardSerializer(services["cards"], many=True).data,
            },
            "timeline_events": UserTimelineSerializer(timeline, many=True).data,
            "explainable_ai": explainability,
            "account_statistics": stats
        }

    @staticmethod
    def export_data_response(user, format_type='json'):
        if not user or not user.is_authenticated:
            return HttpResponse("Unauthorized", status=401)

        data = ExportService.get_full_user_data_dict(user)
        fmt = str(format_type).lower().strip()

        if fmt == 'zip':
            buffer = io.BytesIO()
            with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                # Add JSON dump
                zip_file.writestr("finora_user_data.json", json.dumps(data, indent=2, default=str))
                
                # Add CSV summary
                csv_lines = ["Section,Key,Value"]
                for k, v in data.get("financial_snapshot", {}).items():
                    csv_lines.append(f"Snapshot,{k},{v}")
                for g in data.get("goals", []):
                    csv_lines.append(f"Goal,{g.get('goal_name')},{g.get('current_progress')}/{g.get('target_amount')} ({g.get('status')})")
                zip_file.writestr("finora_summary.csv", "\n".join(csv_lines))
                
                # Add Readme
                zip_file.writestr("README.txt", f"Finora Financial Archive for {user.email}.\nGenerated automatically by Finora Export Service.")
                
            buffer.seek(0)
            response = HttpResponse(buffer.read(), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="finora_user_data_archive.zip"'
            return response

        elif fmt == 'pdf' or fmt == 'text':
            # Generate clean formatted text report (serves as printable PDF text)
            lines = [
                "==========================================================",
                f"           FINORA FINANCIAL IDENTITY ARCHIVE",
                f"           User: {user.email}",
                "==========================================================\n",
                "--- 1. PROFILE DETAILS ---",
                f"Full Name: {data.get('profile', {}).get('full_name')}",
                f"Phone: {data.get('profile', {}).get('phone')}",
                f"Occupation: {data.get('profile', {}).get('occupation')}",
                f"Completion: {data.get('profile', {}).get('completion_percentage')}%\n",
                "--- 2. FINANCIAL SNAPSHOT ---",
                f"Credit Score: {data.get('financial_snapshot', {}).get('credit_score')}",
                f"Risk Profile: {data.get('financial_snapshot', {}).get('risk_profile')}",
                f"Monthly Income: ₹{data.get('financial_snapshot', {}).get('monthly_income')}",
                f"Monthly Savings: ₹{data.get('financial_snapshot', {}).get('monthly_savings')}",
                f"Net Worth: ₹{data.get('financial_snapshot', {}).get('net_worth')}",
                f"Health Score: {data.get('financial_snapshot', {}).get('financial_health_score')}/100\n",
                "--- 3. FINANCIAL GOALS ---"
            ]
            for g in data.get("goals", []):
                lines.append(f"• {g.get('goal_name')} — ₹{g.get('current_progress')}/₹{g.get('target_amount')} [{g.get('status')}] (Primary: {g.get('is_primary')})")
            lines.append("\n--- 4. EXPLAINABLE AI SUMMARY ---")
            lines.append(data.get("explainable_ai", {}).get("summary_text", ""))
            
            content = "\n".join(lines)
            response = HttpResponse(content, content_type='text/plain; charset=utf-8')
            response['Content-Disposition'] = 'attachment; filename="finora_identity_report.txt"'
            return response

        else:
            # Default JSON
            response = HttpResponse(json.dumps(data, indent=2, default=str), content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="finora_user_data.json"'
            return response
