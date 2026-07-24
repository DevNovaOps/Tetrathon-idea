"""
Generators for the Credit Score Module.
Each class has a single responsibility for mapping metrics to specific UI sections.
"""
import math
from decimal import Decimal
from .constants import IDEAL_SAVINGS_RATIO, IDEAL_EXPENSE_RATIO_MAX, FEATURE_LABELS, MIN_SCORE, MAX_SCORE

class HistoryGenerator:
    """Generates realistic synthetic score history with a gradual progression."""
    
    def __init__(self, final_score: int):
        self.final_score = final_score
        
    def generate(self) -> list:
        # Instead of random jumps, simulate a gradual climb or dip over 7 months
        # based on a logarithmic or smooth curve leading up to the final score.
        history = []
        months = 7
        # Assume the user started slightly lower 6 months ago, maybe 30-60 points lower.
        # Use modulo arithmetic on final_score to generate a deterministic "start delta".
        start_delta = 25 + (self.final_score % 30) 
        start_score = max(MIN_SCORE, self.final_score - start_delta)
        
        for i in range(months):
            # Smooth exponential approach to final score
            progress = (i / (months - 1)) ** 1.5 
            current = start_score + int((self.final_score - start_score) * progress)
            
            # Add a tiny deterministic jitter (-2 to +2)
            jitter = (self.final_score + i) % 5 - 2 
            current = min(MAX_SCORE, max(MIN_SCORE, current + jitter))
            history.append(current)
            
        # Ensure the last element matches the final score exactly
        history[-1] = self.final_score
        return history

class BreakdownGenerator:
    """Maps sub-scores to the UI breakdown cards with dynamic descriptions."""
    
    def __init__(self, scores: dict):
        self.scores = scores
        self.color_map = {
            "payment_behaviour": {"bg": "green-bg", "text": "green-text", "hex": "#10B981", "icon": "💳"},
            "savings_habit": {"bg": "blue-bg", "text": "blue-text", "hex": "#3B82F6", "icon": "🏦"},
            "financial_stability": {"bg": "purple-bg", "text": "purple-text", "hex": "#A855F7", "icon": "📊"},
            "investment_behaviour": {"bg": "cyan-bg", "text": "cyan-text", "hex": "#06B6D4", "icon": "📈"},
            "upi_activity": {"bg": "indigo-bg", "text": "indigo-text", "hex": "#6366F1", "icon": "📱"},
            "utility_bills": {"bg": "emerald-bg", "text": "emerald-text", "hex": "#059669", "icon": "⚡"},
        }

    def _get_description(self, key: str, score: int) -> str:
        if key == "payment_behaviour":
            if score >= 80: return "Outstanding debt management with near-perfect payment history."
            if score >= 50: return "Average payment history; consolidate active loans to improve."
            return "Multiple active loans or missed payments are impacting your score."
        if key == "savings_habit":
            if score >= 80: return "Excellent savings habits, maintaining a strong safety net."
            if score >= 50: return "Moderate savings levels. Aim to increase monthly contributions."
            return "Savings reserves are low and require immediate attention."
        if key == "financial_stability":
            if score >= 80: return "High financial stability driven by low expenses and strong reserves."
            if score >= 50: return "Stable financial footing, but vulnerable to unexpected shocks."
            return "High expense ratio or lack of emergency funds reduces stability."
        if key == "investment_behaviour":
            if score >= 80: return "Active, diversified investment portfolio driving long-term wealth."
            if score >= 50: return "Standard investment footprint. Consider diversifying assets."
            return "Minimal investment activity. Start regular SIPs to build resilience."
        if key == "upi_activity":
            if score >= 80: return "High digital footprint showing strong financial engagement."
            if score >= 50: return "Moderate digital transaction volume."
            return "Low UPI usage restricts alternative data analysis."
        if key == "utility_bills":
            if score >= 80: return "100% on-time utility payments signal high reliability."
            if score >= 50: return "Occasional delays in utility payments noted."
            return "Frequent late payments are significantly hurting this metric."
        return ""
        
    def generate(self) -> list:
        breakdown = []
        for key, val in self.scores.items():
            label = FEATURE_LABELS.get(key, key)
            c = self.color_map.get(key, self.color_map["payment_behaviour"])
            breakdown.append({
                "key": key,
                "title": label,
                "percentage": val,
                "description": self._get_description(key, val),
                "icon": c["icon"],
                "bg_class": c["bg"],
                "text_class": c["text"],
                "hex_color": c["hex"]
            })
        return breakdown

class ExplanationGenerator:
    """Generates AI Explanations using exact real numerical values."""
    
    def __init__(self, metrics_data: dict, profile):
        self.raw = metrics_data.get("raw", {})
        self.profile = profile
        
    def generate(self) -> dict:
        return {
            "positive_factors": self._get_positive_factors(),
            "negative_factors": self._get_negative_factors(),
            "ai_explanations": self._get_ai_explanations()
        }
        
    def _get_positive_factors(self) -> list:
        factors = []
        if self.profile.bill_payment_habit == 'Always on time':
            factors.append({"name": "On-time Utility Bill Payments", "impact_text": "High Impact", "badge_color": "green"})
        if self.profile.existing_loans == 'None':
            factors.append({"name": "Zero Active Debt", "impact_text": "High Impact", "badge_color": "green"})
        if self.profile.upi_usage in ['Daily', 'Multiple times a day']:
            factors.append({"name": "Active Digital Footprint", "impact_text": "Medium", "badge_color": "blue"})
        if self.raw["expense_ratio"] <= IDEAL_EXPENSE_RATIO_MAX:
            factors.append({"name": "Healthy Expense Ratio", "impact_text": "High Impact", "badge_color": "green"})
        return factors

    def _get_negative_factors(self) -> list:
        factors = []
        if self.profile.bill_payment_habit == 'Frequently late':
            factors.append({"name": "Late Bill Payments", "impact_text": "Reduce", "badge_color": "orange"})
        if self.profile.existing_loans == 'Multiple Loans':
            factors.append({"name": "High Debt Burden", "impact_text": "High Impact", "badge_color": "orange"})
        if self.raw["emergency_fund_coverage"] < 3:
            factors.append({"name": "Low Emergency Fund", "impact_text": "Build Up", "badge_color": "orange"})
        if self.raw["expense_ratio"] > 0.5:
            factors.append({"name": "High Expense Ratio", "impact_text": "Reduce", "badge_color": "orange"})
        return factors

    def _get_ai_explanations(self) -> list:
        explanations = []
        
        income = self.raw.get("income", 0)
        expenses = self.raw.get("expenses", 0)
        savings = self.raw.get("savings", 0)
        investment = self.raw.get("investment", 0)
        
        # Expenses vs Income
        if income > 0:
            expense_pct = int(self.raw["expense_ratio"] * 100)
            if expense_pct <= 50:
                explanations.append({
                    "title": f"Monthly expenses consume only {expense_pct}% of income.",
                    "desc": "Strong cash flow improves financial stability and leaves room for investments.",
                    "icon_color": "green",
                    "icon_type": "check"
                })
            else:
                explanations.append({
                    "title": f"Expenses consume {expense_pct}% of your income.",
                    "desc": "Reducing discretionary spending will significantly boost your score and stability.",
                    "icon_color": "orange",
                    "icon_type": "alert"
                })
                
        # Savings Ratio
        if savings > 0 and income > 0:
            months_worth = savings / income
            if months_worth >= 2:
                explanations.append({
                    "title": f"Savings equal {months_worth:.1f} months of income.",
                    "desc": "This significantly strengthens your emergency reserve and reduces risk.",
                    "icon_color": "blue",
                    "icon_type": "sparkle"
                })
            else:
                explanations.append({
                    "title": f"Total savings (₹{int(savings):,}) provide limited runway.",
                    "desc": "Aim to save at least 2-6 months of income to protect against financial shocks.",
                    "icon_color": "orange",
                    "icon_type": "alert"
                })

        # Investments
        if investment > 0 and income > 0:
            inv_pct = int(self.raw["investment_ratio"] * 100)
            explanations.append({
                "title": f"Current investment ratio is {inv_pct}%.",
                "desc": f"Consistent monthly investments of ₹{int(investment):,} improve long-term financial resilience.",
                "icon_color": "purple",
                "icon_type": "trend"
            })
            
        # Emergency Fund
        ef = self.raw.get("emergency_fund_coverage", 0)
        if ef >= 6:
            explanations.append({
                "title": "Emergency fund is fully funded.",
                "desc": "Having 6+ months of expenses saved provides a solid financial safety net.",
                "icon_color": "cyan",
                "icon_type": "shield"
            })
        elif ef > 0:
            explanations.append({
                "title": "Emergency fund is partially funded.",
                "desc": "Continue building your reserve until it reaches at least six months of expenses.",
                "icon_color": "blue",
                "icon_type": "shield"
            })
            
        # Default fallback if too few explanations
        if len(explanations) < 4:
            explanations.append({
                "title": "Consistent financial habits build credit.",
                "desc": "Keep paying bills on time, saving regularly, and investing to see continuous growth.",
                "icon_color": "blue",
                "icon_type": "sparkle"
            })
            
        return explanations[:8]

class RecommendationGenerator:
    """Generates structured, prioritized recommendations."""
    
    def __init__(self, metrics_data: dict, profile):
        self.raw = metrics_data.get("raw", {})
        self.scores = metrics_data.get("scores", {})
        self.profile = profile
        
    def generate(self) -> dict:
        sorted_metrics = sorted(self.scores.items(), key=lambda x: x[1], reverse=True)
        top_strength_key = sorted_metrics[0][0] if sorted_metrics else ""
        improvement_key = sorted_metrics[-1][0] if sorted_metrics else ""
        
        raw_recs = []
        
        # Priority: Critical
        if self.profile.bill_payment_habit == 'Frequently late':
            raw_recs.append({
                "priority": "Critical",
                "reason": "Late bill payments severely damage your credit history.",
                "desc": "Automate utility bill payments to ensure 100% on-time record.",
                "benefit": "Instantly improves reliability signals to lenders.",
                "impact": "+30-40 points"
            })
            
        if self.profile.existing_loans == 'Multiple Loans':
            raw_recs.append({
                "priority": "Critical",
                "reason": "High active debt burdens reduce your borrowing capacity.",
                "desc": "Consolidate active loans to reduce overall interest and monthly outflows.",
                "benefit": "Lowers debt-to-income ratio significantly.",
                "impact": "+25-35 points"
            })
            
        # Priority: High
        if self.raw.get("emergency_fund_coverage", 0) < 3:
            raw_recs.append({
                "priority": "High",
                "reason": "Low emergency reserves increase vulnerability to shocks.",
                "desc": "Increase emergency fund to cover at least three to six months of expenses.",
                "benefit": "Prevents the need for high-interest borrowing during crises.",
                "impact": "+15-20 points"
            })
            
        if self.raw.get("expense_ratio", 0) > 0.5:
            raw_recs.append({
                "priority": "High",
                "reason": "High discretionary spending limits your wealth-building capacity.",
                "desc": "Reduce discretionary spending to improve monthly cash flow.",
                "benefit": "Frees up capital for investments and debt repayment.",
                "impact": "+10-15 points"
            })
            
        # Priority: Medium
        if self.raw.get("investment_ratio", 0) < 0.10:
            raw_recs.append({
                "priority": "Medium",
                "reason": "Investment ratio is below the recommended 10-20% threshold.",
                "desc": "Start or increase monthly SIPs to at least 10% of your income.",
                "benefit": "Builds long-term financial resilience and AI scoring.",
                "impact": "+5-10 points"
            })

        # Priority: Low / Maintenance
        if not raw_recs:
            raw_recs.append({
                "priority": "Low",
                "reason": "Your profile demonstrates excellent financial health.",
                "desc": "Maintain current financial habits and avoid new debt.",
                "benefit": "Sustains your excellent score.",
                "impact": "+1-5 points"
            })
            
        # Sort by priority
        priority_order = {"Critical": 1, "High": 2, "Medium": 3, "Low": 4}
        raw_recs.sort(key=lambda x: priority_order.get(x["priority"], 99))
        
        # We will return the structured dictionaries instead of strings
        # The frontend JS will be updated to handle these strings by combining them
        actionable_steps = []
        for r in raw_recs:
            # We construct a rich string that the JS can parse or display directly
            actionable_steps.append(f"<b>{r['priority']} Priority</b>: {r['desc']}<br><br><b>Reason</b>: {r['reason']}<br><b>Benefit</b>: {r['benefit']}<br><b>Impact</b>: <span style='color:#10B981;font-weight:bold;'>{r['impact']}</span>")

        return {
            "top_strength": FEATURE_LABELS.get(top_strength_key, "General"),
            "improvement_opportunity": FEATURE_LABELS.get(improvement_key, "None"),
            "actionable_steps": actionable_steps
        }
