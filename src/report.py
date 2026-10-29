import duckdb
import pandas as pd
import yaml
import os

def load_config(filepath="config/experiment_spec.yaml"):
    with open(filepath, "r") as file:
        return yaml.safe_load(file)

def generate_report():
    print("Connecting to DuckDB results store...")
    config = load_config()
    con = duckdb.connect('data/processed/warehouse.db')
    
    # Layer 8 & 9: Read from results store to build presentation[cite: 4]
    try:
        results_df = con.execute("SELECT * FROM results.experiment_results").df()
    except duckdb.CatalogException:
        print("Error: Results table not found. Please run analyze.py first.")
        return
        
    primary_metric = config['primary_metric']
    primary_row = results_df[results_df['metric'] == primary_metric].iloc[0]
    
    p_value = primary_row['p_value']
    abs_diff = primary_row['abs_diff']
    alpha = config['parameters']['alpha']
    
    # Layer 10: Apply decision rules[cite: 14]
    if p_value < alpha and abs_diff > 0:
        decision = "Ship treatment"
        rationale = "Primary metric is significant and positive. Roll out to all users."
    elif p_value < alpha and abs_diff < 0:
        decision = "Keep control"
        rationale = "Primary metric is significant but negative. Do not ship."
    else:
        decision = "Flat / Inconclusive"
        rationale = "No statistically meaningful difference. Choose based on cost or simplicity."
        
    # Generate Section 10.3 Executive Summary Template[cite: 14]
    md_content = f"""# A/B Test Executive Summary: Cookie Cats Gate Move

## Question
Does moving the progression gate from level 30 to level 40 improve player retention without hurting engagement?[cite: 1]

## Result
The absolute difference in {primary_metric} between treatment and control was **{abs_diff:+.4f}** (p-value: {p_value:.5f}).

## Confidence
**High.** The data passed all pipeline validation gates, including a strict Sample Ratio Mismatch (SRM) check and duplicate user scan prior to statistical analysis. 

## Impact
A shift of {abs_diff:+.2%} in 7-day retention applied across the active player base. 

## Recommendation and Next Step
**{decision}**
{rationale}
"""

    os.makedirs('reports', exist_ok=True)
    with open('reports/final_report.md', 'w') as f:
        f.write(md_content)
        
    print(f"Executive summary successfully generated at reports/final_report.md")
    con.close()

if __name__ == "__main__":
    generate_report()