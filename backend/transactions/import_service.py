"""
Transaction import service — CSV import, demo data generation, manual CRUD.
"""
import csv
import io
import random
from datetime import date, timedelta
from decimal import Decimal

from .models import Transaction
from .classification_engine import TransactionClassifier


class TransactionImportService:

    # ── Manual CRUD ───────────────────────────────────────────────────

    @staticmethod
    def create_transaction(user, data: dict) -> Transaction:
        """Create a single transaction with auto-classification."""
        merchant = data.get('merchant', '')
        description = data.get('description', '')
        amount = float(data.get('amount', 0))

        classification = TransactionClassifier.classify(merchant, description, amount)

        tx = Transaction.objects.create(
            user=user,
            amount=abs(Decimal(str(amount))),
            merchant=merchant,
            category=data.get('category') or classification['category'],
            original_category=classification['category'],
            date=data.get('date', date.today()),
            payment_method=data.get('payment_method', 'upi'),
            location=data.get('location', ''),
            description=description,
            source=data.get('source', 'manual'),
            is_income=data.get('is_income', classification['is_income']),
        )
        return tx

    @staticmethod
    def correct_category(user, tx_id, new_category: str):
        """Manually correct a transaction's category."""
        try:
            tx = Transaction.objects.get(id=tx_id, user=user, is_deleted=False)
            if not tx.original_category:
                tx.original_category = tx.category
            tx.category = new_category
            tx.save()
            return tx
        except Transaction.DoesNotExist:
            return None

    @staticmethod
    def delete_transaction(user, tx_id):
        try:
            tx = Transaction.objects.get(id=tx_id, user=user, is_deleted=False)
            tx.is_deleted = True
            tx.save()
            return True
        except Transaction.DoesNotExist:
            return False

    # ── CSV Import ────────────────────────────────────────────────────

    @staticmethod
    def import_csv(user, file_content: str) -> dict:
        """
        Import transactions from CSV.
        Expected columns: date, amount, merchant, description, payment_method
        """
        reader = csv.DictReader(io.StringIO(file_content))
        created = 0
        errors = []

        for i, row in enumerate(reader):
            try:
                merchant = row.get('merchant', row.get('Merchant', ''))
                desc = row.get('description', row.get('Description', ''))
                amount = float(row.get('amount', row.get('Amount', 0)))
                classification = TransactionClassifier.classify(merchant, desc, amount)

                # Parse date
                date_str = row.get('date', row.get('Date', ''))
                try:
                    tx_date = date.fromisoformat(date_str)
                except (ValueError, TypeError):
                    tx_date = date.today()

                Transaction.objects.create(
                    user=user,
                    amount=abs(Decimal(str(amount))),
                    merchant=merchant,
                    category=row.get('category', classification['category']),
                    original_category=classification['category'],
                    date=tx_date,
                    payment_method=row.get('payment_method', 'upi'),
                    location=row.get('location', ''),
                    description=desc,
                    source='csv_import',
                    is_income=classification['is_income'],
                )
                created += 1
            except Exception as e:
                errors.append(f"Row {i + 1}: {str(e)}")

        return {"imported": created, "errors": errors}

    # ── Demo Data Generation ──────────────────────────────────────────

    @staticmethod
    def generate_demo_data(user, months: int = 6) -> dict:
        """Generate realistic synthetic transactions for demo/judging."""
        if Transaction.objects.filter(user=user, source='demo').exists():
            return {"message": "Demo data already exists", "count": 0}

        today = date.today()
        transactions = []

        # Monthly recurring income
        INCOME_TEMPLATES = [
            {'merchant': 'Employer Payroll', 'category': 'salary', 'amount_range': (35000, 85000), 'method': 'bank_transfer'},
            {'merchant': 'Freelance Client', 'category': 'freelance', 'amount_range': (5000, 25000), 'method': 'upi'},
        ]

        # Monthly recurring expenses
        RECURRING_EXPENSES = [
            {'merchant': 'Landlord Rent', 'category': 'rent', 'amount_range': (8000, 20000), 'method': 'bank_transfer'},
            {'merchant': 'Airtel Broadband', 'category': 'utilities', 'amount_range': (599, 1499), 'method': 'upi'},
            {'merchant': 'Jio Mobile Recharge', 'category': 'utilities', 'amount_range': (199, 999), 'method': 'upi'},
            {'merchant': 'Netflix Subscription', 'category': 'subscriptions', 'amount_range': (199, 649), 'method': 'credit_card'},
            {'merchant': 'HDFC Life Insurance', 'category': 'insurance', 'amount_range': (1500, 5000), 'method': 'bank_transfer'},
            {'merchant': 'Home Loan EMI', 'category': 'emi', 'amount_range': (12000, 25000), 'method': 'bank_transfer'},
        ]

        # Variable daily expenses
        VARIABLE_EXPENSES = [
            {'merchant': 'Swiggy', 'category': 'food', 'amount_range': (150, 800), 'method': 'upi'},
            {'merchant': 'Zomato', 'category': 'food', 'amount_range': (200, 1200), 'method': 'upi'},
            {'merchant': 'BigBasket', 'category': 'groceries', 'amount_range': (500, 3000), 'method': 'upi'},
            {'merchant': 'Blinkit', 'category': 'groceries', 'amount_range': (100, 800), 'method': 'upi'},
            {'merchant': 'Amazon Shopping', 'category': 'shopping', 'amount_range': (299, 8000), 'method': 'credit_card'},
            {'merchant': 'Flipkart', 'category': 'shopping', 'amount_range': (199, 5000), 'method': 'debit_card'},
            {'merchant': 'Uber Cab', 'category': 'transport', 'amount_range': (80, 500), 'method': 'upi'},
            {'merchant': 'Ola Auto', 'category': 'transport', 'amount_range': (50, 300), 'method': 'upi'},
            {'merchant': 'Indian Oil Petrol', 'category': 'transport', 'amount_range': (500, 3000), 'method': 'debit_card'},
            {'merchant': 'PVR Cinemas', 'category': 'entertainment', 'amount_range': (250, 1500), 'method': 'upi'},
            {'merchant': 'Apollo Pharmacy', 'category': 'health', 'amount_range': (100, 2000), 'method': 'upi'},
            {'merchant': 'Decathlon Sports', 'category': 'shopping', 'amount_range': (500, 4000), 'method': 'credit_card'},
            {'merchant': 'Starbucks Coffee', 'category': 'food', 'amount_range': (250, 600), 'method': 'upi'},
            {'merchant': 'Zerodha SIP', 'category': 'investment', 'amount_range': (1000, 10000), 'method': 'bank_transfer'},
            {'merchant': 'Groww Mutual Fund', 'category': 'investment', 'amount_range': (500, 5000), 'method': 'upi'},
            {'merchant': 'Electricity Board', 'category': 'utilities', 'amount_range': (800, 3000), 'method': 'upi'},
            {'merchant': 'Water Supply Bill', 'category': 'utilities', 'amount_range': (200, 800), 'method': 'upi'},
            {'merchant': 'Local Kirana Store', 'category': 'groceries', 'amount_range': (50, 500), 'method': 'cash'},
            {'merchant': 'Chai Point', 'category': 'food', 'amount_range': (30, 150), 'method': 'upi'},
            {'merchant': 'MakeMyTrip', 'category': 'travel', 'amount_range': (2000, 15000), 'method': 'credit_card'},
        ]

        LOCATIONS = [
            'Mumbai', 'Delhi', 'Bengaluru', 'Hyderabad', 'Pune',
            'Chennai', 'Kolkata', 'Jaipur', 'Ahmedabad', 'Online',
        ]

        for month_offset in range(months):
            month_date = today - timedelta(days=30 * month_offset)

            # Income (1-2 per month)
            for inc in INCOME_TEMPLATES:
                if inc['category'] == 'freelance' and random.random() > 0.6:
                    continue
                tx_date = month_date.replace(day=min(random.choice([1, 5, 10, 15]), 28))
                amount = random.randint(inc['amount_range'][0], inc['amount_range'][1])
                transactions.append(Transaction(
                    user=user, amount=Decimal(str(amount)), merchant=inc['merchant'],
                    category=inc['category'], original_category=inc['category'],
                    date=tx_date, payment_method=inc['method'],
                    location=random.choice(LOCATIONS[:3]),
                    description=f"{inc['merchant']} — {inc['category']} credited",
                    source='demo', is_income=True,
                ))

            # Recurring expenses (all monthly)
            for exp in RECURRING_EXPENSES:
                if exp['category'] == 'emi' and random.random() > 0.5:
                    continue
                tx_date = month_date.replace(day=min(random.choice([1, 5, 7, 10, 15, 20]), 28))
                amount = random.randint(exp['amount_range'][0], exp['amount_range'][1])
                transactions.append(Transaction(
                    user=user, amount=Decimal(str(amount)), merchant=exp['merchant'],
                    category=exp['category'], original_category=exp['category'],
                    date=tx_date, payment_method=exp['method'],
                    location=random.choice(LOCATIONS),
                    description=f"{exp['merchant']} monthly payment",
                    source='demo', is_income=False,
                ))

            # Variable expenses (8-15 per month)
            num_variable = random.randint(8, 15)
            chosen = random.sample(VARIABLE_EXPENSES, min(num_variable, len(VARIABLE_EXPENSES)))
            for exp in chosen:
                day = random.randint(1, 28)
                tx_date = month_date.replace(day=day)
                amount = random.randint(exp['amount_range'][0], exp['amount_range'][1])
                transactions.append(Transaction(
                    user=user, amount=Decimal(str(amount)), merchant=exp['merchant'],
                    category=exp['category'], original_category=exp['category'],
                    date=tx_date, payment_method=exp['method'],
                    location=random.choice(LOCATIONS),
                    description=f"Payment to {exp['merchant']}",
                    source='demo', is_income=False,
                ))

        Transaction.objects.bulk_create(transactions)
        return {"message": "Demo data generated", "count": len(transactions)}
