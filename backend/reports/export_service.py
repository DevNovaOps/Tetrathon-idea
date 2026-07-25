class ExportService:
    @staticmethod
    def generate_export_link(report_type):
        return {
            "status": "success",
            "message": f"Export for {report_type} generated successfully.",
            "url": f"/media/exports/mock_{report_type}.pdf"
        }
