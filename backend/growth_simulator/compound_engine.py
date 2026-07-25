class CompoundEngine:
    """
    Handles deterministic financial math formulas for compounding.
    """
    @staticmethod
    def calculate_future_value(monthly_sip: int, years: int, annual_cagr: float) -> int:
        if monthly_sip <= 0 or years <= 0:
            return 0
        
        months = years * 12
        monthly_rate = (annual_cagr / 100) / 12
        
        # Formula: FV = P * [ ((1 + r)^n - 1) / r ] * (1 + r)
        fv = monthly_sip * (((1 + monthly_rate)**months - 1) / monthly_rate) * (1 + monthly_rate)
        return int(fv)

    @staticmethod
    def calculate_metrics(monthly_sip: int, years: int, annual_cagr: float) -> dict:
        total_invested = monthly_sip * years * 12
        future_value = CompoundEngine.calculate_future_value(monthly_sip, years, annual_cagr)
        estimated_returns = max(0, future_value - total_invested)
        return {
            "total_invested": total_invested,
            "estimated_returns": estimated_returns,
            "future_value": future_value
        }
