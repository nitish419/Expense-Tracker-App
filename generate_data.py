import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

def generate_synthetic_data(num_records=500):
    categories = ['Food & Dining', 'Transportation', 'Rent/Mortgage', 'Utilities', 'Entertainment', 'Shopping', 'Healthcare']
    payment_methods = ['Credit Card', 'Debit Card', 'Cash', 'UPI']
    
    data = []
    start_date = datetime.today() - timedelta(days=365) # 1 year of data
    
    for _ in range(num_records):
        date = start_date + timedelta(days=random.randint(0, 365))
        category = random.choice(categories)
        
        # Assign realistic amounts based on category
        if category == 'Rent/Mortgage':
            amount = round(random.uniform(500, 1500), 2)
        elif category in ['Food & Dining', 'Shopping']:
            amount = round(random.uniform(10, 150), 2)
        else:
            amount = round(random.uniform(20, 300), 2)
            
        method = random.choice(payment_methods)
        
        data.append([date.strftime('%Y-%m-%d'), category, amount, method])
        
    df = pd.DataFrame(data, columns=['Date', 'Category', 'Amount', 'Payment_Method'])
    
    # Ensure data folder exists
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/synthetic_expenses.csv', index=False)
    print("✅ Synthetic dataset created successfully at 'data/synthetic_expenses.csv'")

if __name__ == "__main__":
    generate_synthetic_data()