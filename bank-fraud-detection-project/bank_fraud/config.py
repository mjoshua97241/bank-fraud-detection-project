from pathlib import Path
import os

# Determine the project root dynamically
# This assumes config.py is located at bank_fraud/config.py
# So, we go up two levels from config.py to reach the project root
# bank_fraud/config.py -> bank_fraud/ -> project_root/
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# --- Data Directories ---
DATA_DIR = PROJECT_ROOT / 'data'
RAW_DATA_DIR = DATA_DIR / 'raw'
INTERIM_DATA_DIR = DATA_DIR / 'interim'
PROCESSED_DATA_DIR = DATA_DIR / 'processed'
EXTERNAL_DATA_DIR = DATA_DIR / 'external'

# --- Other Important Directories (add as needed) ---
NOTEBOOKS_DIR = PROJECT_ROOT / 'notebooks'
MODELS_DIR = PROJECT_ROOT / 'models'
REPORTS_DIR = PROJECT_ROOT / 'reports'
REPORTS_FIGURES_DIR = REPORTS_DIR / 'figures'
REFERENCES_DIR = PROJECT_ROOT / 'references'

# --- Specific File Paths (add as needed) ---
RAW_ANONYMIZED_DATASET = RAW_DATA_DIR / 'anonymized_output_dataset.parquet'
INTERIM_DATASET_V01 = INTERIM_DATA_DIR / '0.01_dataset.parquet'
INTERIM_EDA_DATASET = INTERIM_DATA_DIR / '1.0_initial_eda_dataset.parquet'
DATA_DICTIONARIES_DIR = REFERENCES_DIR

# Example of how to use it in a notebook:
# from bank_fraud.config import RAW_ANONYMIZED_DATASET
# df = pd.read_parquet(RAW_ANONYMIZED_DATASET)