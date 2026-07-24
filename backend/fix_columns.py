import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    try:
        cursor.execute("ALTER TABLE user_profiles MODIFY monthly_income DECIMAL(12, 2) NULL")
        cursor.execute("ALTER TABLE user_profiles MODIFY monthly_expenses DECIMAL(12, 2) NULL")
        cursor.execute("ALTER TABLE user_profiles MODIFY savings DECIMAL(12, 2) NULL")
        cursor.execute("ALTER TABLE user_profiles MODIFY monthly_investment_budget DECIMAL(12, 2) NULL")
        print("Columns altered successfully.")
    except Exception as e:
        print("Error altering columns:", e)
