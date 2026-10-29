# 🧪 Automated A/B Test Analysis & Decision Pipeline

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![DuckDB](https://img.shields.io/badge/DuckDB-In--Memory_Warehouse-yellow.svg)](https://duckdb.org/)
[![SQL](https://img.shields.io/badge/SQL-Data_Transformation-lightgrey.svg)]()
[![Status](https://img.shields.io/badge/Status-Production_Ready-success.svg)]()

## 📌 Overview
This repository contains a production-grade, automated A/B test analysis pipeline. Moving beyond static Jupyter Notebooks, this system implements a strict 10-layer architecture that separates data ingestion, SQL-based metric transformation, data quality validation, and statistical computation. 

The pipeline ensures that no business decision is ever made on corrupted data by enforcing a strict Validation Gate (checking for Sample Ratio Mismatch and assignment leakage) before any p-values are calculated.

## 📖 Table of Contents
- [Business Context](#business-context)
- [System Architecture](#system-architecture)
- [Key Engineering Features](#key-engineering-features)
- [Repository Structure](#repository-structure)
- [Quick Start & Installation](#quick-start--installation)
- [Example Automated Output](#example-automated-output)
- [Author](#author)

## 🏢 Business Context
A/B testing is often plagued by "p-hacking," novelty effects, and broken logging. This system addresses these industry challenges by:
1. **Pre-registering metrics:** Locking in hypotheses, Minimum Detectable Effect (MDE), and significance thresholds (Alpha) in a YAML configuration file before data is analyzed.
2. **Automating Governance:** Removing human bias by programmatically translating statistical outputs into definitive "Ship," "Keep Control," or "Inconclusive" recommendations.

## ⚙️ System Architecture
The pipeline follows a modern ELT (Extract, Load, Transform) pattern combined with a statistical engine:

1. **Ingestion & Storage (DuckDB):** Raw user assignments and events are loaded into an in-memory DuckDB warehouse.
2. **Data Transformation (SQL):** Raw tables are immutable. Staging and User-Metric marts are built strictly via SQL to ensure relational integrity and deduplication.
3. **Validation Gate (Python/SciPy):** A critical checkpoint that runs Chi-Square Goodness-of-Fit tests for Sample Ratio Mismatch (SRM). Pipeline execution halts immediately if $p < 0.001$.
4. **Statistical Engine (Statsmodels):** Computes Two-Proportion Z-Tests for binary metrics (e.g., retention) and Welch's T-Tests for continuous metrics (e.g., engagement).
5. **Presentation Layer (Markdown):** Automatically generates a stakeholder-ready executive summary.

## 🚀 Key Engineering Features
* **Config-Driven Execution:** Entire experiments can be modified by altering `experiment_spec.yaml` without touching the core Python codebase.
* **Separation of Concerns:** Transformation logic lives in SQL; statistical logic lives in Python.
* **Reproducibility:** A single execution script runs the pipeline end-to-end, guaranteeing identical results on every run.

## 📂 Repository Structure
```text
ab-test-pipeline/
├── config/
│   └── experiment_spec.yaml      # Experiment parameters (MDE, Alpha, Metrics)
├── data/
│   ├── raw/                      # Immutable raw extracts (CSV)
│   └── processed/                # DuckDB warehouse storage
├── reports/
│   └── final_report.md           # Auto-generated executive summaries
├── sql/
│   ├── 01_staging.sql            # Deduplication and schema enforcement
│   └── 02_user_metrics.sql       # Aggregation into analysis-ready mart
├── src/
│   ├── generate_mock_data.py     # Generates a 10k user synthetic dataset
│   ├── ingest.py                 # Loads raw data into the DuckDB warehouse
│   ├── validate.py               # Validation Gate (SRM and duplicate checks)
│   ├── analyze.py                # Hypothesis testing engine
│   └── report.py                 # Markdown decision generator
├── .gitignore
├── requirements.txt
└── README.md