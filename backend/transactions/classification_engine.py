"""
Keyword-based auto-classification engine for transactions.
Maps merchant names and descriptions to spending categories.
"""


# ── Keyword → Category mappings ──────────────────────────────────────
CLASSIFICATION_RULES = {
    'salary': {
        'keywords': ['salary', 'payroll', 'wage', 'stipend', 'neft-salary'],
        'is_income': True,
    },
    'freelance': {
        'keywords': ['freelance', 'upwork', 'fiverr', 'consulting', 'client payment', 'invoice'],
        'is_income': True,
    },
    'investment_income': {
        'keywords': ['dividend', 'interest', 'mutual fund', 'fd maturity', 'capital gain'],
        'is_income': True,
    },
    'refund': {
        'keywords': ['refund', 'cashback', 'reversal', 'return credit'],
        'is_income': True,
    },
    'groceries': {
        'keywords': ['bigbasket', 'blinkit', 'zepto', 'dmart', 'reliance fresh',
                     'grocery', 'supermarket', 'kirana', 'vegetables', 'fruits', 'more supermarket'],
        'is_income': False,
    },
    'food': {
        'keywords': ['swiggy', 'zomato', 'restaurant', 'cafe', 'pizza', 'burger',
                     'dominos', 'mcdonald', 'kfc', 'starbucks', 'chai', 'biryani',
                     'food', 'dining', 'canteen', 'mess', 'dhaba', 'bakery'],
        'is_income': False,
    },
    'transport': {
        'keywords': ['uber', 'ola', 'rapido', 'metro', 'bus', 'train', 'irctc',
                     'petrol', 'diesel', 'fuel', 'parking', 'toll', 'auto',
                     'cab', 'rickshaw', 'flight', 'indigo', 'air india'],
        'is_income': False,
    },
    'entertainment': {
        'keywords': ['netflix', 'prime video', 'hotstar', 'spotify', 'youtube premium',
                     'movie', 'cinema', 'pvr', 'inox', 'gaming', 'xbox', 'playstation',
                     'bookmyshow', 'concert', 'event'],
        'is_income': False,
    },
    'shopping': {
        'keywords': ['amazon', 'flipkart', 'myntra', 'ajio', 'nykaa', 'meesho',
                     'snapdeal', 'mall', 'clothing', 'shoes', 'electronics',
                     'croma', 'reliance digital', 'decathlon'],
        'is_income': False,
    },
    'utilities': {
        'keywords': ['electricity', 'water', 'gas', 'broadband', 'wifi', 'internet',
                     'jio', 'airtel', 'vi ', 'bsnl', 'recharge', 'mobile bill',
                     'phone bill', 'dth', 'tata play', 'postpaid'],
        'is_income': False,
    },
    'health': {
        'keywords': ['hospital', 'doctor', 'pharmacy', 'medical', 'apollo', 'medplus',
                     'medicine', 'lab test', 'health', 'dental', 'clinic',
                     'practo', 'pharmeasy', 'netmeds', '1mg'],
        'is_income': False,
    },
    'education': {
        'keywords': ['school', 'college', 'tuition', 'course', 'udemy', 'coursera',
                     'coaching', 'books', 'stationery', 'exam', 'university'],
        'is_income': False,
    },
    'investment': {
        'keywords': ['mutual fund', 'sip', 'stocks', 'zerodha', 'groww', 'upstox',
                     'kuvera', 'ppf', 'nps', 'fd', 'fixed deposit', 'gold',
                     'sovereign gold', 'sgb', 'etf'],
        'is_income': False,
    },
    'rent': {
        'keywords': ['rent', 'house rent', 'flat rent', 'pg rent', 'hostel',
                     'accommodation', 'maintenance', 'society'],
        'is_income': False,
    },
    'emi': {
        'keywords': ['emi', 'loan', 'home loan', 'car loan', 'personal loan',
                     'education loan', 'credit card bill', 'cc payment'],
        'is_income': False,
    },
    'insurance': {
        'keywords': ['insurance', 'lic', 'premium', 'term plan', 'health insurance',
                     'car insurance', 'policy', 'hdfc life', 'icici prudential'],
        'is_income': False,
    },
    'subscriptions': {
        'keywords': ['subscription', 'membership', 'gym', 'club', 'saas',
                     'apple', 'google one', 'icloud', 'linkedin premium'],
        'is_income': False,
    },
    'travel': {
        'keywords': ['hotel', 'oyo', 'makemytrip', 'goibibo', 'booking.com',
                     'airbnb', 'travel', 'vacation', 'tour', 'trip'],
        'is_income': False,
    },
    'transfer': {
        'keywords': ['transfer', 'self transfer', 'neft', 'rtgs', 'imps',
                     'upi transfer'],
        'is_income': False,
    },
}


class TransactionClassifier:
    """Deterministic keyword-based transaction classifier."""

    @staticmethod
    def classify(merchant: str, description: str = '', amount: float = 0) -> dict:
        """
        Returns {'category': str, 'is_income': bool} based on keyword matching.
        Checks merchant first, then description.
        """
        text = f"{merchant} {description}".lower().strip()

        for category, config in CLASSIFICATION_RULES.items():
            for keyword in config['keywords']:
                if keyword.lower() in text:
                    return {
                        'category': category,
                        'is_income': config['is_income'],
                    }

        # Fallback: guess income vs expense from amount context
        if amount > 0 and any(w in text for w in ['received', 'credited', 'income', 'cr']):
            return {'category': 'other_income', 'is_income': True}

        return {'category': 'other', 'is_income': False}
