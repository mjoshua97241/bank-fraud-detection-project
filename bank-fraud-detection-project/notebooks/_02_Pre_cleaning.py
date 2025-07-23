#%% [markdown]
# # Cleaning (Sequential Processing Optimized)
# 
# The pipeline processes a large dataset (e.g., combined EFT data) by loading it, cleaning it, and filtering it to remove potential data leakage, ultimately producing a refined dataset suitable for model training.

# %%[markdown]
# ## Step 0: Import Libraries and Setup
import pandas as pd
import numpy as np
import os
from pathlib import Path
import pyarrow.parquet as pq
from tqdm import tqdm
import logging
import time
import sys

# Import progress bar utilities
import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils import progress_file_loader, progress_file_reader

# Import memory monitoring (keeping this for performance tracking)
from parallel_utils import monitor_memory_usage

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# %%
# Check current working directory context
print("Current working directory:", os.getcwd())
print("Script location:", Path(__file__).parent.resolve())
print("Using optimized sequential processing")

# %%[markdown]
# ## Step 1: Load Data (Sequential Optimized)
# Load the combined EFT data from the interim directory

# %%
@monitor_memory_usage
def load_data_sequential():
    """Load data with memory monitoring."""
    logger.info("Step 1: Loading data...")
    
    # Define the exact path as specified
    data_path = Path(r"E:\Personal\Full_Stack_Data_Analyst\Data_Science\Eskwelabs\Capstone Project\01_Code_Notebooks\01_Capstone_Project\data\interim\combined_eft_data.parquet")
    
    # Load data with progress tracking
    print(f"Loading data from: {data_path}")
    start_time = time.time()
    df = pd.read_parquet(data_path)
    load_time = time.time() - start_time
    
    logger.info(f"Data loaded successfully in {load_time:.2f} seconds. Shape: {df.shape}")
    print(f"Initial dataset shape: {df.shape}")
    print(f"Columns: {len(df.columns)}")
    print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024 / 1024:.1f} MB")
    
    return df

df = load_data_sequential()

# %% [markdown]
# ## Check some columns only
df['txn_velocity_accel_wk2'].value_counts()

# %% [markdown]
# ## Drop columns that are not needed


# %%[markdown]
# ## Step 2: Parse Dates & Filter by Date (Sequential Optimized)
# Cast datetime columns and filter by date threshold using vectorized operations

# %%
@monitor_memory_usage
def parse_dates_and_filter_sequential(df):
    """Parse dates and filter with optimized sequential processing."""
    logger.info("Step 2: Parsing dates and applying date filter...")
    start_time = time.time()
    
    # Convert datetime columns using vectorized operations
    print("Converting datetime columns...")
    df = df.copy()  # Work on a copy to avoid SettingWithCopyWarning
    
    # Vectorized datetime conversion (much faster than chunked processing)
    df['orig_onboarded_datetime'] = pd.to_datetime(df['orig_onboarded_datetime'])
    df['date_tagged'] = pd.to_datetime(df['date_tagged'])
    
    # Filter rows where orig_onboarded_datetime ≤ 2025-05-11
    print("Applying date filter...")
    cutoff_date = pd.to_datetime('2025-05-11')
    initial_count = len(df)
    df = df[df['orig_onboarded_datetime'] <= cutoff_date]
    filtered_count = len(df)
    
    processing_time = time.time() - start_time
    logger.info(f"Date parsing and filtering completed in {processing_time:.2f} seconds")
    logger.info(f"Date filtering: {initial_count} → {filtered_count} rows ({initial_count - filtered_count} removed)")
    print(f"After date filtering: {df.shape}")
    
    return df

df = parse_dates_and_filter_sequential(df)

# %%[markdown]
# ## Step 3: Filter Tags (Sequential Optimized)
# Remove KYC holds and keep only confirmed fraud and non-fraud cases

# %%
@monitor_memory_usage
def filter_tags_sequential(df):
    """Filter tags with optimized sequential processing."""
    logger.info("Step 3: Filtering tags...")
    start_time = time.time()
    
    # Check current tag distribution
    print("Current dna_final_tag distribution:")
    print(df['dna_final_tag'].value_counts())
    
    initial_count = len(df)
    
    # Vectorized filtering operations
    print("Applying tag filters...")
    # Drop rows where dna_final_tag == "KYC_HOLD"
    df = df[df['dna_final_tag'] != 'KYC_HOLD']
    
    # Keep only rows with dna_final_tag in {"CONFIRMED_FRAUD", "NON_FRAUD"}
    df = df[df['dna_final_tag'].isin(['CONFIRMED_FRAUD', 'NON_FRAUD'])]
    
    final_count = len(df)
    processing_time = time.time() - start_time
    
    logger.info(f"Tag filtering completed in {processing_time:.2f} seconds")
    logger.info(f"Tag filtering: {initial_count} → {final_count} (removed {initial_count - final_count})")
    print(f"After tag filtering: {df.shape}")
    print("Final tag distribution:")
    print(df['dna_final_tag'].value_counts())
    
    return df

df = filter_tags_sequential(df)

# %%[markdown]
# ## Step 4: Remove fraud cases that are 7 days old from orig_onboarded_datetime
# Remove transactions close to fraud tagging date to avoid data leakage

# %%
@monitor_memory_usage
def remove_fraud_cases_sequential(df):
    logger.info('Step 4: Removing CONFIRMED_FRAUD cases within 7 days of orig_onboarded_datetime...')
    start_time = time.time()
    
    # Filter for CONFIRMED_FRAUD cases first
    fraud_df = df[df['dna_final_tag'] == 'CONFIRMED_FRAUD'].copy()
    
    if not fraud_df.empty:
        # Calculate date difference in days using vectorized operations
        fraud_df['days_difference'] = (fraud_df['date_tagged'] - fraud_df['orig_onboarded_datetime']).dt.days
        
        # Remove rows where days_difference <= 7
        initial_fraud_count = len(fraud_df)
        fraud_df = fraud_df[fraud_df['days_difference'] > 7]
        final_fraud_count = len(fraud_df)
        
        # Merge back the filtered fraud cases into the original dataframe
        df = df[df['dna_final_tag'] != 'CONFIRMED_FRAUD']  # Remove all CONFIRMED_FRAUD first
        df = pd.concat([df, fraud_df], ignore_index=True)  # Add back the filtered ones
        
        logger.info(f'Removed {initial_fraud_count - final_fraud_count} CONFIRMED_FRAUD cases within 7 days')
        logger.info(f'Step 4 completed in {(time.time() - start_time):.2f} seconds')
        print(f'After Step 4: {df.shape}')
    else:
        logger.info('No CONFIRMED_FRAUD cases to process')
    
    return df

df = remove_fraud_cases_sequential(df)

# %% [markdown]
# ## Step 5: Filter Zero Transaction Profiles
# Remove profiles with no PESONET or INSTAPAY transactions

# %%
@monitor_memory_usage
def filter_zero_transactions_sequential(df):
    """Filter out profiles with zero PESONET and INSTAPAY transactions."""
    logger.info("Step 5: Filtering out profiles with zero PESONET and INSTAPAY transactions...")
    start_time = time.time()
    
    # Check if we have the required columns
    required_columns = ['count_PESONET_IN', 'count_PESONET_OUT', 'count_INSTAPAY_IN', 'count_INSTAPAY_OUT']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        logger.warning(f"Missing columns for zero transaction filtering: {missing_columns}")
        logger.warning("Skipping zero transaction filtering step")
        return df
    
    # Count before filtering
    initial_count = len(df)
    
    # Apply the filter - keep only rows where at least one of these columns has a non-zero value
    mask = (
        (df['count_PESONET_IN'] > 0) | 
        (df['count_PESONET_OUT'] > 0) | 
        (df['count_INSTAPAY_IN'] > 0) | 
        (df['count_INSTAPAY_OUT'] > 0)
    )
    
    # Apply the filter
    df = df[mask]
    
    # Count after filtering
    final_count = len(df)
    removed_count = initial_count - final_count
    
    # Log results
    processing_time = time.time() - start_time
    logger.info(f"Zero transaction filtering completed in {processing_time:.2f} seconds")
    logger.info(f"Zero transaction filtering: {initial_count} → {final_count} (removed {removed_count} rows)")
    print(f"After zero transaction filtering: {df.shape}")
    
    return df

df = filter_zero_transactions_sequential(df)

# %% [markdown]
# ## Step 6: Drop Redundant Columns (account_number, orig_onboarded_date, date_restricted)
# Drop redundant columns

# %%
@monitor_memory_usage
def drop_redundant_columns_sequential(df):
    """Drop redundant columns with optimized sequential processing."""
    logger.info("Step 6: Dropping redundant columns...")
    start_time = time.time()
    
    # Drop redundant columns
    df = df.drop(columns=['account_number', 'orig_onboarded_date', 'date_restricted'])
    
    logger.info(f"Redundant columns dropped in {time.time() - start_time:.2f} seconds")
    return df

df = drop_redundant_columns_sequential(df)
df.shape

# %% [markdown]
# ## Step 7: Save to cleaned parquet file
file_name = 'cleaned_combined_eft_data.parquet'

df.to_parquet(r"E:\Personal\Full_Stack_Data_Analyst\Data_Science\Eskwelabs\Capstone Project\01_Code_Notebooks\01_Capstone_Project\data\interim\cleaned_combined_eft_data.parquet")

print('Data cleaning process completed successfully.')
print('Data saved to: ', file_name)


# %%
