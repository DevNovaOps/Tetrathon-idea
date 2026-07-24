import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("""
        UPDATE user_profiles 
        SET monthly_income='0.00', monthly_expenses='0.00', savings='0.00', monthly_investment_budget='0.00' 
        WHERE monthly_income='0' OR monthly_income='' OR monthly_income IS NULL
    """)
    print("Database data fixed for migration!")
