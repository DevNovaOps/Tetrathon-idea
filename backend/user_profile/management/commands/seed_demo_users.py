import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with demo users and realistic historical data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Starting demo data generation. This will take a moment...'))
        
        # We will create 3 specific persona users
        personas = [
            {
                "email": "demo_conservative@finora.com",
                "name": "Arjun Patel",
                "risk_profile": "Low",
                "income": 45000,
                "savings_pct": 35, # 35% savings rate
                "score_baseline": 720,
            },
            {
                "email": "demo_moderate@finora.com",
                "name": "Priya Sharma",
                "risk_profile": "Moderate",
                "income": 85000,
                "savings_pct": 20, # 20% savings rate
                "score_baseline": 640,
            },
            {
                "email": "demo_aggressive@finora.com",
                "name": "Kabir Khan",
                "risk_profile": "High",
                "income": 120000,
                "savings_pct": 10, # 10% savings rate (high spend)
                "score_baseline": 550,
            }
        ]
        
        for p in personas:
            self.stdout.write(f"Generating data for {p['email']}...")
            
            # Create User
            user, created = User.objects.get_or_create(
                email=p['email'],
                defaults={
                    'full_name': p['name'],
                    'country': 'IN',
                    'is_active': True,
                }
            )
            if created:
                user.set_password('demo123')
                user.date_joined = timezone.now() - timedelta(days=120) # 4 months ago
                user.save()
            else:
                self.stdout.write(f"  User {p['email']} already exists. Skipping data generation to avoid duplicates.")
                continue
                
            # Setup User Profile
            profile = user.profile
            profile.monthly_income = p['income']
            profile.monthly_expenses = int(p['income'] * (1 - (p['savings_pct'] / 100)))
            profile.savings = p['income'] - profile.monthly_expenses
            # Modifiers based on persona
            if p['savings_pct'] > 30:
                profile.bill_payment_habit = 'Always on time'
                profile.existing_loans = 'None'
                profile.monthly_investment_budget = profile.monthly_income * 0.30
            elif p['savings_pct'] > 15:
                profile.bill_payment_habit = 'Occasionally late'
                profile.existing_loans = 'Home Loan'
                profile.monthly_investment_budget = profile.monthly_income * 0.15
            else:
                profile.bill_payment_habit = 'Frequently late'
                profile.existing_loans = 'Credit Card Debt'
                profile.monthly_investment_budget = profile.monthly_income * 0.05
                
            profile.save()
            
            # Generate Transactions (6 months)
            from transactions.import_service import TransactionImportService
            TransactionImportService.generate_demo_data(user, months=6)
            
            # Create a Financial Goal
            from user_profile.models import FinancialGoal
            target = p['income'] * 5
            FinancialGoal.objects.create(
                user=user,
                goal_name="Emergency Fund" if p['risk_profile'] == 'Low' else ("Car Downpayment" if p['risk_profile'] == 'Moderate' else "Stock Portfolio"),
                goal_type='Emergency Fund' if p['risk_profile'] == 'Low' else ('Vehicle' if p['risk_profile'] == 'Moderate' else 'Wealth Creation'),
                target_amount=target,
                current_progress=target * random.uniform(0.1, 0.4),
                monthly_contribution=profile.savings * 0.5,
                priority='High',
                is_primary=True,
                deadline=timezone.now().date() + timedelta(days=365)
            )
            
            # Trigger Pipelines
            self.stdout.write("  Triggering analytical pipelines...")
            from user_profile.services.snapshot_service import SnapshotService
            SnapshotService.record_snapshot(user)
            
            from risk_profile.orchestrator import RiskProfileOrchestrator
            RiskProfileOrchestrator.run_pipeline(user)
            
            from credit_score.services import CreditScoreService
            CreditScoreService.get_or_calculate_credit_profile(user)
            
            from investment.orchestrator import InvestmentOrchestrator
            InvestmentOrchestrator.run_pipeline(user)
            
            from reports.report_service import ReportService
            # Generate a report for previous month
            prev_month = timezone.now().date() - timedelta(days=30)
            ReportService.get_full_report(user, prev_month.month, prev_month.year)
            
            self.stdout.write(self.style.SUCCESS(f"Successfully generated data for {p['name']}"))

        self.stdout.write(self.style.SUCCESS('\nDemo data generation complete!'))
        self.stdout.write("Test accounts:")
        self.stdout.write("1. demo_conservative@finora.com / demo123 (High savings, Low Risk)")
        self.stdout.write("2. demo_moderate@finora.com / demo123 (Medium savings, Moderate Risk)")
        self.stdout.write("3. demo_aggressive@finora.com / demo123 (Low savings, High Risk, Late Payments)")
