"""
Feature Engineering Pipeline for Digital Signals.
Derives 5 composite features from raw signal data, each scored 0-100.
"""


class DigitalFeatureEngine:
    """
    Deterministic feature derivation from DigitalSignalProfile fields.
    No randomness — all scores are pure functions of stored values.
    """

    # ── Lookup tables (value → score) ─────────────────────────────────
    BILL_SCORE = {
        'always_on_time': 100,
        'occasionally_late': 50,
        'frequently_late': 15,
        'no_bills': 40,          # neutral — no signal, not negative
    }

    RECHARGE_SCORE = {
        'monthly': 90,
        'prepaid': 85,
        'quarterly': 60,
        'irregular': 30,
    }

    BROADBAND_SCORE = {
        'always_on_time': 100,
        'occasionally_late': 50,
        'no_broadband': 40,
    }

    DIGITAL_TX_SCORE = {
        'multiple_daily': 100,
        'daily': 85,
        'weekly': 60,
        'rarely': 30,
        'never': 5,
    }

    SHOPPING_SCORE = {
        'weekly': 90,
        'biweekly': 75,
        'monthly': 55,
        'rarely': 25,
    }

    REGULARITY_SCORE = {
        'excellent': 100,
        'good': 75,
        'average': 45,
        'poor': 15,
    }

    SPENDING_SCORE = {
        'high': 90,
        'moderate': 70,
        'low': 40,
        'minimal': 15,
    }

    def __init__(self, signal_profile):
        self.sp = signal_profile

    # ── Derived Features ──────────────────────────────────────────────

    def utility_payment_consistency(self) -> int:
        """Average of all utility + broadband bill payment scores."""
        scores = [
            self.BILL_SCORE.get(self.sp.electricity_bill_frequency, 40),
            self.BILL_SCORE.get(self.sp.water_bill_frequency, 40),
            self.BILL_SCORE.get(self.sp.gas_bill_frequency, 40),
            self.BROADBAND_SCORE.get(self.sp.broadband_payment, 40),
            self.RECHARGE_SCORE.get(self.sp.mobile_recharge_frequency, 40),
        ]
        return min(100, int(sum(scores) / len(scores)))

    def digital_payment_usage(self) -> int:
        """Measures how actively the user uses UPI and card payments."""
        upi = self.DIGITAL_TX_SCORE.get(self.sp.upi_transaction_frequency, 30)
        card = self.DIGITAL_TX_SCORE.get(self.sp.card_transaction_frequency, 30)
        return min(100, int(upi * 0.6 + card * 0.4))

    def cash_dependency(self) -> int:
        """Inverse of digital payment usage — higher = more cash dependent = worse."""
        return max(0, 100 - self.digital_payment_usage())

    def ecommerce_behaviour(self) -> int:
        """Composite of online shopping frequency and spending behaviour."""
        shop = self.SHOPPING_SCORE.get(self.sp.shopping_frequency, 40)
        online = self.SPENDING_SCORE.get(self.sp.online_spending_behaviour, 40)
        return min(100, int(shop * 0.5 + online * 0.5))

    def digital_financial_activity(self) -> int:
        """
        Weighted master score across all derived features.
        Weights: utility 30%, digital payment 30%, ecommerce 20%, regularity 20%
        """
        utility = self.utility_payment_consistency()
        digital = self.digital_payment_usage()
        ecom = self.ecommerce_behaviour()
        regularity = self.REGULARITY_SCORE.get(self.sp.utility_payment_regularity, 45)
        return min(100, int(
            utility * 0.30 +
            digital * 0.30 +
            ecom * 0.20 +
            regularity * 0.20
        ))

    # ── Public API ────────────────────────────────────────────────────

    def calculate_all(self) -> dict:
        """Returns all 5 derived feature scores."""
        return {
            "utility_payment_consistency": self.utility_payment_consistency(),
            "digital_payment_usage": self.digital_payment_usage(),
            "cash_dependency": self.cash_dependency(),
            "ecommerce_behaviour": self.ecommerce_behaviour(),
            "digital_financial_activity": self.digital_financial_activity(),
        }

    def credit_score_contribution(self) -> int:
        """
        Single 0-100 score consumed by the Credit Scoring Engine.
        Mirrors the digital_financial_activity but can be weighted differently.
        """
        return self.digital_financial_activity()
