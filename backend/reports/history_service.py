class HistoryService:
    @staticmethod
    def get_available_months():
        # Simulated available months for the dropdown filter
        return [
            {"value": "2024-07", "label": "July 2024"},
            {"value": "2024-06", "label": "June 2024"},
            {"value": "2024-05", "label": "May 2024"},
            {"value": "2024-04", "label": "April 2024"}
        ]

class ExportService:
    @staticmethod
    def generate_export_link(report_type):
        # Mock export generation
        return {
            "status": "success",
            "message": f"Export for {report_type} generated successfully.",
            "url": f"/media/exports/mock_{report_type}.pdf"
        }
