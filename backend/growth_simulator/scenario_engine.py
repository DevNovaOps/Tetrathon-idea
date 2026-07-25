class ScenarioEngine:
    """
    Generates scenario parameters based on the base expected CAGR.
    """
    @staticmethod
    def generate_scenarios(base_cagr: float) -> list:
        # e.g. base_cagr could be 12.0
        # Conservative = base - 4%, Moderate = base, Aggressive = base + 4%
        return [
            {
                "id": "conservative",
                "name": "Conservative Scenario",
                "desc": "Debt funds & fixed-income focus for high capital protection.",
                "cagr": max(2.0, base_cagr - 4.0),
                "icon": "🛡️",
                "color": "orange"
            },
            {
                "id": "moderate",
                "name": "Moderate Scenario (Recommended)",
                "desc": "Balanced equity & debt mix for optimal growth.",
                "cagr": base_cagr,
                "icon": "⚖️",
                "color": "blue"
            },
            {
                "id": "aggressive",
                "name": "Aggressive Scenario",
                "desc": "Equity index & blue-chip stock heavy allocation for maximum return.",
                "cagr": min(25.0, base_cagr + 4.0),
                "icon": "🚀",
                "color": "purple"
            }
        ]
