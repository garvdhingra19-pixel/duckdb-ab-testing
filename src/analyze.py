import duckdb
import pandas as pd
import yaml
from statsmodels.stats.proportion import proportions_ztest
from scipy.stats import ttest_ind
from validate import run_validation_gate

def load_config(filepath="config/experiment_spec.yaml"):
    with open(filepath, "r") as file:
        return yaml.safe_load(file)

def run_ztest(df, metric, variants):
    successes = [df[df['variant'] == var][metric].sum() for var in variants]
    nobs = [df[df['variant'] == var][metric].count() for var in variants]
    stat, pval = proportions_ztest(successes, nobs)
    
    return {
        "metric": metric,
        "control_value": float(successes[0] / nobs[0]),
        "treatment_value": float(successes[1] / nobs[1]),
        "abs_diff": float((successes[1] / nobs[1]) - (successes[0] / nobs[0])),
        "p_value": float(pval)
    }

def run_ttest(df, metric, variants):
    control_data = df[df['variant'] == variants[0]][metric]
    treatment_data = df[df['variant'] == variants[1]][metric]
    stat, pval = ttest_ind(control_data, treatment_data, equal_var=False)
    
    return {
        "metric": metric,
        "control_value": float(control_data.mean()),
        "treatment_value": float(treatment_data.mean()),
        "abs_diff": float(treatment_data.mean() - control_data.mean()),
        "p_value": float(pval)
    }

def analyze_experiment():
    config = load_config()
    variants = config['variants']
    
    print("Connecting to DuckDB mart...")
    con = duckdb.connect('data/processed/warehouse.db')
    
    # Layer 4 Output: Querying the mart[cite: 3]
    df = con.execute("SELECT * FROM mart.user_metrics").df()
    
    # Layer 6: Validation Gate[cite: 5]
    print("Running Validation Gate...")
    run_validation_gate(df) # Ensure validate.py expects 'variant' and 'user_id'
    
    print("\n--- Running Layer 7: Statistical Engine ---") #[cite: 3]
    results = []
    
    results.append(run_ztest(df, config['primary_metric'], variants))
    for metric in config['secondary_metrics']:
        if metric in ['retained_d1']:
            results.append(run_ztest(df, metric, variants))
        else:
            results.append(run_ttest(df, metric, variants))
            
    results_df = pd.DataFrame(results)
    print(results_df.to_string(index=False))
    
    # Layer 8: Results Store[cite: 4]
    print("\nSaving to Layer 8: Results Store...")
    con.execute("CREATE SCHEMA IF NOT EXISTS results;")
    con.execute("CREATE OR REPLACE TABLE results.experiment_results AS SELECT * FROM results_df")
    con.close()

if __name__ == "__main__":
    analyze_experiment()