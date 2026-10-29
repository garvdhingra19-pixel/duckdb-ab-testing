import duckdb
import pandas as pd
import os

def build_warehouse():
    print("Initializing DuckDB warehouse...")
    # Layer 3: Warehouse (DuckDB)[cite: 3, 5]
    os.makedirs('data/processed', exist_ok=True)
    con = duckdb.connect('data/processed/warehouse.db')
    
    # Create schemas
    con.execute("CREATE SCHEMA IF NOT EXISTS raw;")
    con.execute("CREATE SCHEMA IF NOT EXISTS stg;")
    con.execute("CREATE SCHEMA IF NOT EXISTS mart;")
    
    # Layer 2: Ingestion[cite: 3, 5]
    print("Loading data to raw schema...")
    # Assuming standard Cookie Cats CSV is present
    df = pd.read_csv('data/raw/cookie_cats.csv')
    
    # Since Cookie Cats is a flat file, we simulate the relational raw tables required by the architecture[cite: 7]
    assignments = df[['userid', 'version']].copy()
    assignments['assigned_at'] = '2026-01-01 00:00:00' # Simulated timestamp
    assignments.columns = ['user_id', 'variant', 'assigned_at']
    
    events_d1 = df[['userid', 'retention_1']].rename(columns={'userid': 'user_id'})
    events_d1['event_name'] = 'return_day_1'
    events_d1['event_ts'] = '2026-01-02 00:00:00'
    events_d1 = events_d1[events_d1['retention_1'] == True]
    
    events_d7 = df[['userid', 'retention_7']].rename(columns={'userid': 'user_id'})
    events_d7['event_name'] = 'return_day_7'
    events_d7['event_ts'] = '2026-01-08 00:00:00'
    events_d7 = events_d7[events_d7['retention_7'] == True]
    
    events_rounds = df[['userid', 'sum_gamerounds']].rename(columns={'userid': 'user_id'})
    events_rounds['event_name'] = 'game_round'
    events_rounds['event_ts'] = '2026-01-01 12:00:00'
    
    events = pd.concat([events_d1, events_d7, events_rounds])[['user_id', 'event_name', 'event_ts']]
    events['value'] = 1
    
    con.execute("CREATE OR REPLACE TABLE raw.assignments AS SELECT * FROM assignments")
    con.execute("CREATE OR REPLACE TABLE raw.events AS SELECT * FROM events")
    
    # Layer 4: Transformation[cite: 3]
    print("Running SQL transformations...")
    with open('sql/01_staging.sql', 'r') as f:
        con.execute(f.read())
    with open('sql/02_user_metrics.sql', 'r') as f:
        con.execute(f.read())
        
    print("Warehouse built successfully. Mart is ready.")
    con.close()

if __name__ == "__main__":
    build_warehouse()