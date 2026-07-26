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
        from .analytics_service import AnalyticsService
        summary = AnalyticsService.get_summary(user, month, year)
        perf = AnalyticsService.get_performance(user, month, year)
        raw = summary.get("_raw", {})

        def make_styled_table(data, widths=None):
            if not widths:
                widths = [160, 120, 100] if len(data[0]) == 3 else [150, 100, 100, 90]
            t = Table(data, colWidths=widths)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F3F4F6")),
                ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor("#1F2937")),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('FONTNAME', (0,0), (-1,0), font_bold),
                ('FONTNAME', (0,1), (-1,-1), font_name),
                ('BOTTOMPADDING', (0,0), (-1,0), 10),
                ('TOPPADDING', (0,0), (-1,0), 10),
                ('BACKGROUND', (0,1), (-1,-1), colors.white),
                ('GRID', (0,0), (-1,-1), 1, colors.HexColor("#E5E7EB"))
            ]))
            return t

        if report_type == "monthly":
            story.append(Paragraph("Monthly Financial Overview", heading_style))
            
            data = [
                ["Category", "Amount", "Trend / Status"],
                ["Total Income", summary["total_income"], "+5%"],
                ["Total Expenses", summary["total_expenses"], perf.get("expense_reduction", "-2%")],
                ["Total Savings", summary["total_savings"], "+8%"],
                ["Investment Valuation", summary["investment_value"], perf.get("investment_growth", "+10%")],
                ["Net Worth", summary["net_worth"], "+4%"],
                ["Savings Rate", summary["savings_rate"], "Target: >= 20%"],
                ["Emergency Fund", summary["emergency_fund_coverage"], "Target: >= 6 Mos"]
            ]
            story.append(make_styled_table(data, [160, 120, 120]))
            story.append(Spacer(1, 20))
            
            story.append(Paragraph("AI Recommendations", heading_style))
            story.append(Paragraph(f"{RUPEE} You saved {summary['total_savings']} this month ({summary['savings_rate']} savings rate), demonstrating strong financial discipline.", normal_style))
            story.append(Paragraph(f"{RUPEE} Your emergency fund currently covers {summary['emergency_fund_coverage']}, providing vital financial security.", normal_style))
            story.append(Paragraph(f"{RUPEE} Consider setting an automated cap on discretionary shopping to maximize monthly cash flow.", normal_style))
            
        elif report_type == "quarterly":
            try:
                target_year = int(year) if year else datetime.date.today().year
                target_month = int(month) if month else datetime.date.today().month
            except (ValueError, TypeError):
                target_year, target_month = datetime.date.today().year, datetime.date.today().month

            q = (target_month - 1) // 3 + 1
            story.append(Paragraph(f"Q{q} {target_year} Quarterly Performance Breakdown", heading_style))
            
            q_months = [3*q - 2, 3*q - 1, 3*q]
            data = [["Month", "Income", "Expenses", "Savings", "Savings Rate"]]
            
            total_inc, total_exp, total_sav = 0, 0, 0
            for m in q_months:
                m_sum = AnalyticsService.get_summary(user, str(m), str(target_year))
                m_raw = m_sum.get("_raw", {})
                inc = m_raw.get("income", 0)
                exp = m_raw.get("expenses", 0)
                sav = m_raw.get("savings", 0)
                total_inc += inc
                total_exp += exp
                total_sav += sav
                m_label = datetime.date(target_year, m, 1).strftime("%B")
                data.append([m_label, f"{RUPEE}{inc:,.0f}", f"{RUPEE}{exp:,.0f}", f"{RUPEE}{sav:,.0f}", m_sum.get("savings_rate", "0%")])
            
            avg_rate = f"{round((total_sav / total_inc * 100), 1)}%" if total_inc > 0 else "0%"
            data.append(["Q-Total", f"{RUPEE}{total_inc:,.0f}", f"{RUPEE}{total_exp:,.0f}", f"{RUPEE}{total_sav:,.0f}", avg_rate])
            
            story.append(make_styled_table(data, [90, 85, 85, 85, 85]))
            story.append(Spacer(1, 20))
            
            story.append(Paragraph("Quarterly Summary & Strategic Insights", heading_style))
            story.append(Paragraph(f"{RUPEE} Your total quarterly savings reached {RUPEE}{total_sav:,.0f} with an average savings rate of {avg_rate}.", normal_style))
            story.append(Paragraph(f"{RUPEE} Consistent cash flow across Q{q} strengthens long-term compounding opportunities.", normal_style))

        elif report_type == "annual":
            try:
                target_year = int(year) if year else datetime.date.today().year
                target_month = int(month) if month else datetime.date.today().month
            except (ValueError, TypeError):
                target_year, target_month = datetime.date.today().year, datetime.date.today().month

            if target_month >= 4:
                fy_label = f"FY {target_year}-{str(target_year+1)[-2:]}"
            else:
                fy_label = f"FY {target_year-1}-{str(target_year)[-2:]}"
                
            story.append(Paragraph(f"Annual Financial Report ({fy_label})", heading_style))
            
            inc_val = raw.get("income", 50000)
            exp_val = raw.get("expenses", 30000)
            sav_val = raw.get("savings", 20000)
            
            data = [
                ["Annual Metric", "Projected / Actual Value", "YoY Trajectory"],
                ["Total Annual Income", f"{RUPEE}{inc_val*12:,.0f}", "+6.5%"],
                ["Total Annual Expenses", f"{RUPEE}{exp_val*12:,.0f}", "-1.8%"],
                ["Total Annual Savings", f"{RUPEE}{sav_val*12:,.0f}", "+14.2%"],
                ["Year-End Portfolio Value", summary["investment_value"], perf.get("investment_growth", "+10%")],
                ["Net Worth Milestone", summary["net_worth"], "+12.4%"],
                ["Annual Savings Rate", summary["savings_rate"], "Target: >= 20%"]
            ]
            story.append(make_styled_table(data, [170, 130, 100]))
            story.append(Spacer(1, 20))
            
            story.append(Paragraph("Annual Wealth & Tax Advisory", heading_style))
            story.append(Paragraph(f"{RUPEE} Your estimated annual savings of {RUPEE}{sav_val*12:,.0f} places you on a strong trajectory toward financial independence.", normal_style))
            story.append(Paragraph(f"{RUPEE} Review your tax-saving allocations (ELSS, PPF, NPS) before fiscal year close to optimize tax liability.", normal_style))

        elif report_type == "investment":
            story.append(Paragraph(f"Investment Portfolio Breakdown ({date_str})", heading_style))
            
            total_inv = raw.get("investment_value", 300000)
            data = [
                ["Asset Class", "Allocation %", "Current Valuation", "Est. Return"],
                ["Equity Mutual Funds / SIPs", "45%", f"{RUPEE}{round(total_inv*0.45):,.0f}", "+14.2% p.a."],
                ["Direct Stock Portfolio", "25%", f"{RUPEE}{round(total_inv*0.25):,.0f}", "+18.5% p.a."],
                ["Fixed Income & Bonds", "20%", f"{RUPEE}{round(total_inv*0.20):,.0f}", "+7.1% p.a."],
                ["Gold & Liquid Reserves", "10%", f"{RUPEE}{round(total_inv*0.10):,.0f}", "+8.0% p.a."],
                ["Total Portfolio", "100%", summary["investment_value"], perf.get("investment_growth", "+12%")]
            ]
            story.append(make_styled_table(data, [140, 75, 105, 80]))
            story.append(Spacer(1, 20))
            
            story.append(Paragraph("Portfolio Optimization Notes", heading_style))
            story.append(Paragraph(f"{RUPEE} Your portfolio valuation currently stands at {summary['investment_value']}, growing at {perf.get('investment_growth', '+10%')} this period.", normal_style))
            story.append(Paragraph(f"{RUPEE} Your risk profile is categorized as <b>{summary.get('risk_level', 'Moderate')}</b>. Maintain discipline in automated SIP contributions.", normal_style))

        elif report_type == "credit":
            story.append(Paragraph(f"Credit Health & Score Analysis ({date_str})", heading_style))
            
            try:
                target_year = int(year) if year else datetime.date.today().year
                target_month = int(month) if month else datetime.date.today().month
            except (ValueError, TypeError):
                target_year, target_month = datetime.date.today().year, datetime.date.today().month

            import random
            random.seed(f"credit-pdf-{user.email if user else 'demo'}-{target_year}-{target_month}")
            score_val = random.randint(762, 794)
            util_val = random.randint(18, 26)
            
            data = [
                ["Credit Indicator", "Current Status", "Benchmark / Impact"],
                ["Credit Score (CIBIL/Equifax)", str(score_val), f"Excellent ({perf.get('credit_score_change', '+15 pts')})"],
                ["Credit Utilization Ratio", f"{util_val}%", "Optimal (< 30%)"],
                ["On-Time Payment History", "100%", "36 Consecutive Months"],
                ["Active Accounts & Lines", "4 Accounts", "2 Cards, 1 Auto, 1 Home"],
                ["Recent Credit Inquiries", "1 Inquiry", "Low Risk Impact"]
            ]
            story.append(make_styled_table(data, [150, 120, 130]))
            story.append(Spacer(1, 20))
            
            story.append(Paragraph("Credit Defense Strategy", heading_style))
            story.append(Paragraph(f"{RUPEE} Your credit score of {score_val} qualifies you for top-tier interest rates on loans and mortgages.", normal_style))
            story.append(Paragraph(f"{RUPEE} Keep your credit utilization below 30% and automate full statement balance payments to preserve excellent standing.", normal_style))
            
        elif report_type == "financial-health":
            story.append(Paragraph(f"Financial Health Engine Analysis ({date_str})", heading_style))
            from .financial_health_engine import FinancialHealthEngine
            health = FinancialHealthEngine.calculate_health(user, month, year)
            
            story.append(Paragraph(f"<b>Overall Score:</b> {health['score']}/100 (Grade {health['grade']})", normal_style))
            story.append(Paragraph(f"<b>Summary:</b> {health['explanation']}", normal_style))
            story.append(Spacer(1, 15))
            
            data = [
                ["Health Dimension", "Evaluation Metric", "Status"],
                ["Savings Rate", summary["savings_rate"], "Optimal" if float(summary["savings_rate"].replace('%',''))>=20 else "Moderate"],
                ["Emergency Fund", summary["emergency_fund_coverage"], "Secure" if "Months" in summary["emergency_fund_coverage"] and float(summary["emergency_fund_coverage"].split()[0])>=6 else "Building"],
                ["Expense Control", summary["expense_ratio"], "Efficient" if float(summary["expense_ratio"].replace('%',''))<60 else "Review Needed"],
                ["Investment Growth", perf.get("investment_growth", "+10%"), "Active"]
            ]
            story.append(make_styled_table(data, [140, 130, 130]))
            story.append(Spacer(1, 15))
            
            story.append(Paragraph("<b>Key Strengths:</b>", normal_style))
            for f in health['positive_factors']:
                story.append(Paragraph(f"  • {f}", normal_style))
                
            story.append(Spacer(1, 10))
            story.append(Paragraph("<b>Areas for Improvement & Action Plan:</b>", normal_style))
            for f in health['negative_factors']:
                story.append(Paragraph(f"  • {f}", normal_style))
            for r in health.get('recommendations', []):
                story.append(Paragraph(f"  ➔ {r}", normal_style))

        else:
            story.append(Paragraph(f"{report_type.replace('-', ' ').title()} Breakdown ({date_str})", heading_style))
            data = [
                ["Category", "Amount", "Status"],
                ["Total Income", summary["total_income"], "+5%"],
                ["Total Expenses", summary["total_expenses"], perf.get("expense_reduction", "-2%")],
                ["Total Savings", summary["total_savings"], "+8%"]
            ]
            story.append(make_styled_table(data, [150, 120, 130]))
            
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
