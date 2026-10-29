import pandas as pd
import yaml
from scipy.stats import chisquare

def load_config(filepath="config/experiment_spec.yaml"):
    with open(filepath, "r") as file:
        return yaml.safe_load(file)

def check_srm(assignments_df, variants, expected_split):
    """
    Runs a Chi-square goodness-of-fit test for Sample Ratio Mismatch[cite: 9].
    Blocks the run if p-value < 0.001[cite: 12].
    """
    # Uses the 'variant' column from the SQL mart
    observed_counts = assignments_df['variant'].value_counts().reindex(variants).fillna(0).values
    total_users = sum(observed_counts)
    expected_counts = [total_users * p for p in expected_split]
    
    stat, p_value = chisquare(f_obs=observed_counts, f_exp=expected_counts)
    
    print(f"SRM Check: Chi-Square Stat = {stat:.2f}, p-value = {p_value:.5f}")
    
    if p_value < 0.001:
        raise ValueError("BLOCKING ERROR: Sample Ratio Mismatch detected (p < 0.001).")
    return True

def check_duplicates(assignments_df):
    """
    Ensures zero users are in more than one variant[cite: 12].
    """
    # Uses the 'user_id' column from the SQL mart
    duplicates = assignments_df['user_id'].duplicated().sum()
    if duplicates > 0:
         raise ValueError(f"BLOCKING ERROR: Found {duplicates} duplicate users.")
    print("Duplicate Check: Passed. No users in multiple variants.")
    return True

def run_validation_gate(df):
    config = load_config()
    
    print("--- Running Validation Gate ---")
    check_duplicates(df)
    check_srm(df, config['variants'], config['expected_split'])
    print("Validation Gate Passed. Ready for statistical engine.")