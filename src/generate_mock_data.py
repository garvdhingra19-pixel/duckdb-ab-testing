import pandas as pd
import numpy as np
import os

def create_mock_data():
    print("Generating mock Cookie Cats data...")
    np.random.seed(42)
    n = 10000 # 10,000 users
    
    data = {
        'userid': range(1, n + 1),
        'version': np.random.choice(['gate_30', 'gate_40'], n),
        'retention_1': np.random.choice([True, False], n, p=[0.45, 0.55]),
        'retention_7': np.random.choice([True, False], n, p=[0.20, 0.80]),
        'sum_gamerounds': np.random.negative_binomial(1, 0.05, n)
    }
    
    df = pd.DataFrame(data)
    os.makedirs('data/raw', exist_ok=True)
    df.to_csv('data/raw/cookie_cats.csv', index=False)
    print("Successfully created data/raw/cookie_cats.csv")

if __name__ == "__main__":
    create_mock_data()