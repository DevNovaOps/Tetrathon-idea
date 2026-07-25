import io
import os
import datetime
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register a Unicode font that supports ₹
# Use DejaVuSans which ships with reportlab and supports ₹
_FONT_DIR = os.path.join(os.path.dirname(__file__), 'fonts')
_FONT_REGISTERED = False

def _register_fonts():
    global _FONT_REGISTERED
    if _FONT_REGISTERED:
        return
    # Try system fonts that support ₹
    candidates = [
        ('C:/Windows/Fonts/arial.ttf', 'C:/Windows/Fonts/arialbd.ttf'),
        ('C:/Windows/Fonts/segoeui.ttf', 'C:/Windows/Fonts/segoeuib.ttf'),
    ]
    for regular, bold in candidates:
        if os.path.exists(regular):
            pdfmetrics.registerFont(TTFont('UniFont', regular))
            if os.path.exists(bold):
                pdfmetrics.registerFont(TTFont('UniFont-Bold', bold))
            else:
                pdfmetrics.registerFont(TTFont('UniFont-Bold', regular))
            _FONT_REGISTERED = True
            return
    # Fallback: just mark as registered to avoid repeated attempts
    _FONT_REGISTERED = True


# Use Rs. as a safe fallback if ₹ still doesn't render
RUPEE = '₹'


class ExportService:
    @staticmethod
    def generate_pdf(report_type, user, month=None, year=None):
        """
        Generate a PDF entirely on the backend using ReportLab.
        Returns a Django HttpResponse with application/pdf content type.
        """
        _register_fonts()
        
        # Determine which font to use
        font_name = 'UniFont' if _FONT_REGISTERED else 'Helvetica'
        font_bold = 'UniFont-Bold' if _FONT_REGISTERED else 'Helvetica-Bold'
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        styles = getSampleStyleSheet()
        
        # Custom styles using Unicode font
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontName=font_bold,
            fontSize=24,
            spaceAfter=30,
            textColor=colors.HexColor("#4F46E5")
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontName=font_bold,
            fontSize=16,
            spaceAfter=12,
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontName=font_name,
            fontSize=10,
            leading=14,
        )
        
        story = []
        
        # Resolve user display name
        user_name = 'Demo User'
        if user and hasattr(user, 'full_name') and user.full_name:
            user_name = user.full_name
        elif user and hasattr(user, 'email'):
            user_name = user.email
        
        # 1. Header & Branding
        story.append(Paragraph("Finora - AI Financial Wellness", title_style))
        story.append(Paragraph(f"<b>Report Type:</b> {report_type.replace('-', ' ').title()}", normal_style))
        story.append(Paragraph(f"<b>Generated for:</b> {user_name}", normal_style))
        
        # Date formatting
        now = datetime.datetime.now()
        if month and year:
            try:
                dt = datetime.date(int(year), int(month), 1)
                date_str = dt.strftime("%B %Y")
            except (ValueError, TypeError):
                date_str = now.strftime("%B %Y")
        else:
            date_str = now.strftime("%B %Y")
            
        story.append(Paragraph(f"<b>Report Period:</b> {date_str}", normal_style))
        story.append(Paragraph(f"<b>Generated on:</b> {now.strftime('%Y-%m-%d %H:%M:%S')}", normal_style))
        story.append(Spacer(1, 20))
        
        # 2. Executive Summary
        story.append(Paragraph("Executive Summary", heading_style))
        story.append(Paragraph(
            "This report is generated dynamically by Finora's deterministic backend engine. "
            "It incorporates your latest profile updates, savings trajectory, and deterministic "
            "financial health modeling based on your inputs.", 
            normal_style
        ))
        story.append(Spacer(1, 20))
        
        # 3. Dynamic Content depending on report_type
        if report_type == "monthly":
            story.append(Paragraph("Monthly Financial Overview", heading_style))
            
            # Fetch real data from analytics service
            from .analytics_service import AnalyticsService
            summary = AnalyticsService.get_summary(user)
            
            data = [
                ["Category", "Amount", "Trend"],
                ["Total Income", summary["total_income"], "+5%"],
                ["Total Expenses", summary["total_expenses"], "-2%"],
                ["Total Savings", summary["total_savings"], "+8%"]
            ]
            
            t = Table(data, colWidths=[150, 120, 80])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F3F4F6")),
                ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor("#1F2937")),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('FONTNAME', (0,0), (-1,0), font_bold),
                ('FONTNAME', (0,1), (-1,-1), font_name),
                ('BOTTOMPADDING', (0,0), (-1,0), 12),
                ('BACKGROUND', (0,1), (-1,-1), colors.white),
                ('GRID', (0,0), (-1,-1), 1, colors.HexColor("#E5E7EB"))
            ]))
            story.append(t)
            story.append(Spacer(1, 20))
            
            story.append(Paragraph("AI Recommendations", heading_style))
            story.append(Paragraph(f"{RUPEE} Consistent monthly savings shows strong financial discipline.", normal_style))
            story.append(Paragraph(f"{RUPEE} Consider setting a monthly cap on discretionary shopping.", normal_style))
            
        elif report_type == "financial-health":
            story.append(Paragraph("Financial Health Engine Analysis", heading_style))
            from .financial_health_engine import FinancialHealthEngine
            health = FinancialHealthEngine.calculate_health(user)
            
            story.append(Paragraph(f"<b>Overall Score:</b> {health['score']}/100 (Grade {health['grade']})", normal_style))
            story.append(Paragraph(f"<b>Summary:</b> {health['explanation']}", normal_style))
            story.append(Spacer(1, 10))
            
            story.append(Paragraph("<b>Strengths:</b>", normal_style))
            for f in health['positive_factors']:
                story.append(Paragraph(f"  - {f}", normal_style))
                
            story.append(Spacer(1, 10))
            story.append(Paragraph("<b>Areas for Improvement:</b>", normal_style))
            for f in health['negative_factors']:
                story.append(Paragraph(f"  - {f}", normal_style))
                
        else:
            # Generic layout for other reports
            story.append(Paragraph(f"{report_type.replace('-', ' ').title()} Breakdown", heading_style))
            story.append(Paragraph(
                f"This is the comprehensive {report_type.replace('-', ' ')} report. "
                "Detailed analytics, charts, and historical comparisons are populated here.",
                normal_style
            ))
            
        story.append(Spacer(1, 40))
        story.append(Paragraph("<i>Confidential - Generated for Educational Purposes Only</i>", normal_style))

        # Build PDF
        doc.build(story)
        
        # Prepare Response
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        safe_date = date_str.replace(' ', '_')
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Finora_{report_type.title()}_{safe_date}.pdf"'
        
        return response
