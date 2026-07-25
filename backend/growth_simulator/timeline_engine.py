class TimelineEngine:
    @staticmethod
    def generate_timeline(monthly_sip: int, cagr: float, future_value: int) -> list:
        return [
            {"icon": "📍", "name": "Today", "sub": "Start SIP"},
            {"icon": "💳", "name": "Monthly SIP", "sub": f"₹{monthly_sip:,} / mo"},
            {"icon": "📈", "name": "Compound Growth", "sub": f"{cagr}% CAGR"},
            {"icon": "🏆", "name": "Goal Achieved", "sub": f"₹{future_value:,} Wealth"}
        ]
