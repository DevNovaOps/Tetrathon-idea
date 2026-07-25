class ProjectionEngine:
    """
    Deterministically calculates future portfolio values based on SIP and CAGR.
    """
    
    @staticmethod
    def calculate_future_value(monthly_sip: int, years: int, cagr: float) -> int:
        """Calculates Future Value of a SIP using standard compound interest."""
        if monthly_sip <= 0 or years <= 0:
            return 0
            
        months = years * 12
        monthly_rate = (cagr / 100) / 12
        
        # FV = P * [ ((1 + r)^n - 1) / r ] * (1 + r)
        fv = monthly_sip * (((1 + monthly_rate)**months - 1) / monthly_rate) * (1 + monthly_rate)
        return int(fv)
