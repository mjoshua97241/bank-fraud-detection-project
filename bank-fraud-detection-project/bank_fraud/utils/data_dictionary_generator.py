import pandas as pd
import numpy as np
from pathlib import Path

# --- Helper Functions ---

def generate_business_description(feature_name, data_type):
    """
    Generates a business context description for a given feature.
    This function contains specific business logic and patterns.
    For a truly generic solution, this part would need to be customized or provided by the user.
    """
    # New engineered features
    if feature_name == 'age_of_person':
        return "Customer age in years calculated from date_of_birth, used for demographic risk profiling"
    elif feature_name == 'survival_days':
        return "Account survival duration in days (from onboarding to restriction), with negative values set to 0"
    elif feature_name == 'account_age':
        return "Account age in days from onboarding to current date, indicating customer tenure regardless of status"

    # Transaction amount and count patterns
    elif 'amt' in feature_name.lower() and 'week' in feature_name:
        return f"Weekly transaction amount for {feature_name.split('_')[-1]} indicating spending behavior patterns"

    elif 'count' in feature_name.lower() and 'week' in feature_name:
        return f"Weekly transaction count for {feature_name.split('_')[-1]} showing account activity frequency"
    elif 'velocity' in feature_name.lower() and 'week' in feature_name:
        return f"Transaction velocity (transactions per day) for {feature_name.split('_')[-1]} indicating account usage intensity"
    elif 'days_active' in feature_name.lower() and 'week' in feature_name:
        return f"Number of active transaction days in {feature_name.split('_')[-1]} showing engagement consistency"

    # Delta and acceleration metrics
    elif 'velocity_delta' in feature_name.lower():
        return "Change in transaction velocity between weeks indicating behavioral shifts or anomalies"
    elif 'velocity_accel' in feature_name.lower():
        return "Transaction velocity acceleration showing rapid behavior changes potentially linked to fraud"
    elif 'dropoff' in feature_name.lower():
        return "Flag indicating significant transaction activity decrease after initial period"

    # 30-day aggregated metrics
    elif '30d' in feature_name:
        if 'count' in feature_name:
            return "Total transaction count over 30-day period showing overall account activity"
        elif 'amt' in feature_name:
            return "Total transaction amount over 30-day period indicating financial flow volume"
        elif 'velocity' in feature_name:
            return "Average daily transaction velocity over 30-day period showing sustained activity level"
        elif 'volatility' in feature_name:
            return "Transaction volatility over 30-day period indicating behavioral consistency or irregularity"

    # Volatility and volume scores
    elif 'vol_score' in feature_name:
        return f"Volatility score for {feature_name.split('_')[-1]} measuring transaction pattern irregularity"

    # Daily transaction extremes
    elif feature_name.startswith('max_') and 'day' in feature_name:
        return f"Maximum daily {feature_name.split('_')[1]} indicating peak account usage or potential abuse"
    elif feature_name.startswith('min_') and 'day' in feature_name:
        return f"Minimum daily {feature_name.split('_')[1]} showing baseline account activity"
    elif feature_name.startswith('avg_') and 'day' in feature_name:
        return f"Average daily {feature_name.replace('avg_', '').replace('_day', '')} indicating typical account behavior"

    # Flow and ratio metrics
    elif 'inflow_outflow_ratio' in feature_name:
        return "Ratio of money flowing in vs out of account indicating account usage type (sink vs pass-through)"
    elif 'net_flow' in feature_name:
        return "Net money flow (in minus out) indicating account balance change patterns"
    elif 'same_day_cico' in feature_name:
        return "Cash-in-cash-out same day patterns potentially indicating money laundering behavior"

    # Payment network specific
    elif 'INSTAPAY' in feature_name:
        network_type = 'InstaPay (real-time) network'
        if 'count' in feature_name:
            direction = 'incoming' if '_IN' in feature_name else 'outgoing'
            return f"Number of {direction} transactions via {network_type} showing payment preference"
        elif 'amount' in feature_name:
            direction = 'received' if '_IN' in feature_name else 'sent'
            return f"Total amount {direction} via {network_type} indicating financial flow volume"
    elif 'PESONET' in feature_name:
        network_type = 'PESONet (batch) network'
        if 'count' in feature_name:
            direction = 'incoming' if '_IN' in feature_name else 'outgoing'
            return f"Number of {direction} transactions via {network_type} showing institutional payment patterns"
        elif 'amount' in feature_name:
            direction = 'received' if '_IN' in feature_name else 'sent'
            return f"Total amount {direction} via {network_type} indicating bulk payment behavior"

    # Time-based behavioral patterns
    elif 'weekend_txn' in feature_name:
        return "Weekend transaction activity indicating non-business hour usage patterns"
    elif 'night_txn' in feature_name:
        return "Nighttime transaction activity potentially indicating suspicious or automated behavior"
    elif 'entropy' in feature_name:
        if 'hour' in feature_name:
            return "Hour-of-day transaction entropy measuring predictability of timing patterns"
        elif 'weekday' in feature_name:
            return "Day-of-week transaction entropy indicating schedule regularity or randomness"

    # Time intervals and sessions
    elif 'time_btwn_txns' in feature_name:
        return "Time intervals between transactions showing account usage rhythm and automation patterns"
    elif 'sessions_per_day' in feature_name:
        return "Transaction sessions per day (grouped by time gaps) indicating user behavior patterns"
    elif 'cv_time_btwn_txns' in feature_name:
        return "Coefficient of variation in transaction timing indicating behavioral consistency"

    # Network and counterparty analysis
    elif 'unique_source' in feature_name or 'unique_destination' in feature_name:
        return "Number of unique counterparties indicating account's network diversity and potential risk"
    elif 'repeat_counterparty_ratio' in feature_name:
        return "Ratio of repeated vs new counterparties indicating relationship-based vs random transaction patterns"
    elif 'entropy' in feature_name and ('source' in feature_name or 'destination' in feature_name):
        return "Counterparty diversity entropy measuring concentration risk and behavioral patterns"
    elif 'top_' in feature_name and 'share' in feature_name:
        return "Concentration of transactions with primary counterparty indicating dependency or control patterns"

    # Profile and demographic features
    elif feature_name == 'profile_id':
        return "Unique customer identifier for linking account activities and fraud investigations"
    elif feature_name == 'account_no':
        return "Primary account number for transaction tracking and customer identification"
    elif feature_name == 'full_name':
        return "Customer full name for identity verification and compliance reporting"
    elif feature_name == 'username':
        return "Digital platform username indicating online banking engagement level"
    elif feature_name == 'date_of_birth':
        return "Customer birth date for age-based risk profiling and regulatory compliance"
    elif feature_name == 'cellphone':
        return "Registered mobile number for customer contact and SMS-based authentication"

    # Onboarding and origination
    elif 'orig_onboarded' in feature_name:
        return "Account opening timestamp for tenure analysis and early fraud detection patterns"
    elif 'orig_channel' in feature_name:
        return "Account opening channel (online/branch) indicating customer acquisition risk profile"
    elif 'orig_os' in feature_name:
        return "Operating system used during account opening indicating device-based risk patterns"
    elif 'origination_type' in feature_name:
        return "Type of account origination process indicating verification level and fraud risk"
    elif 'orig_primary_source_of_funds' in feature_name:
        return "Declared primary income source for AML compliance and risk assessment"
    elif 'orig_industry' in feature_name or 'orig_occupation' in feature_name:
        return "Customer industry/occupation for risk profiling and transaction pattern validation"

    # Card and status information
    elif 'card' in feature_name.lower():
        return "Debit/credit card information indicating payment method preferences and fraud vectors"
    elif 'account_status' in feature_name:
        return "Current account standing indicating operational restrictions or compliance actions"
    elif 'restricted' in feature_name:
        return "Account restriction information for fraud prevention and compliance enforcement"

    # Fraud and compliance tags
    elif 'fraud_tag' in feature_name or 'final_tag' in feature_name:
        return "Fraud classification label for model training and validation purposes"
    elif 'fraud_types' in feature_name:
        return "Specific fraud category for targeted detection and prevention strategies"
    elif 'fraud_channel_source' in feature_name:
        return "Fraud vector identification for channel-specific risk mitigation"
    elif 'ticket_no' in feature_name:
        return "Investigation case identifier for fraud review and audit trail tracking"
    elif 'ops_comments' in feature_name:
        return "Operational notes from fraud analysts providing context for automated detection"

    # Banking and external interactions
    elif 'fila' in feature_name:
        return "FILA (Filipino banking network) interaction data for cross-institution risk assessment"
    elif 'kiosk_interaction' in feature_name:
        return "Physical kiosk usage patterns indicating offline banking behavior and location risk"

    # Contact changes and updates
    elif 'change_email' in feature_name or 'change_mob_num' in feature_name:
        return "Contact information change frequency indicating potential account takeover attempts"

    # Transaction dates and periods
    elif 'first_txn_date' in feature_name or 'last_txn_date' in feature_name:
        return "Transaction timeline boundaries for account lifecycle and dormancy analysis"
    elif 'date_tagged' in feature_name:
        return "Fraud identification date for timeline analysis and detection lag measurement"

    # Generic fallback based on data type
    elif data_type in ['int64', 'float64']:
        return f"Numeric metric related to {feature_name.replace('_', ' ')} for quantitative risk assessment"
    elif data_type == 'object':
        return f"Categorical information for {feature_name.replace('_', ' ')} supporting qualitative risk analysis"
    elif data_type == 'datetime64[ns]':
        return f"Temporal data for {feature_name.replace('_', ' ')} enabling time-based pattern analysis"

    # Final fallback
    return f"Feature {feature_name} providing context for fraud detection and risk assessment"

def partition_features(column_info):
    """
    Partitions features into numeric, categorical, and identifier categories using business logic.
    This function contains specific business logic and patterns.
    For a truly generic solution, this part would need to be customized or provided by the user.
    """
    numeric_features = []
    categorical_features = []
    identifier_features = []

    identifier_patterns = [
        'id', 'account_no', 'account_number', 'source_account_number', 'destination_account_number',
        'full_name', 'username', 'cellphone', 'gr_card_no'
    ]

    binary_flag_patterns = [
        'flag_', '_flag', '_status', 'carded_status', 'card_type', 'origination_type',
        'origination_sub_type', 'orig_channel', 'orig_os', 'athena_fraud_tag', 'final_tag',
        'dna_final_tag', 'fraud_types', 'fraud_channel_source', 'matching_level',
        'imputed', '_imputed'
    ]

    categorical_patterns = [
        'date_', 'datetime_', '_date', '_datetime', 'ticket_no', 'ops_comments',
        'orig_', 'kiosk_', 'fila_', 'acc_mgmt_channel'
    ]

    explicit_numeric_features = [
        'age_of_person', 'survival_days', 'account_age'
    ]

    for col_name, dtype in column_info.items():
        col_lower = col_name.lower()

        if col_name in explicit_numeric_features:
            numeric_features.append(col_name)
        elif any(pattern in col_lower for pattern in identifier_patterns):
            identifier_features.append(col_name)
        elif any(pattern in col_lower for pattern in binary_flag_patterns):
            categorical_features.append(col_name)
        elif dtype in ['object', 'datetime64[ns]']:
            categorical_features.append(col_name)
        elif any(pattern in col_lower for pattern in categorical_patterns):
            categorical_features.append(col_name)
        elif dtype in ['int64', 'float64']:
            if 'txn_days_active_week' in col_lower:
                numeric_features.append(col_name)
            elif 'occurence' in col_lower or 'occurrence' in col_lower:
                numeric_features.append(col_name)
            else:
                numeric_features.append(col_name)
        else:
            categorical_features.append(col_name)

    return numeric_features, categorical_features, identifier_features

def compute_numeric_metadata(df, numeric_features, column_info):
    """Compute comprehensive metadata for numeric features."""
    metadata_list = []

    numeric_df_subset = df[[f for f in numeric_features if f in df.columns]]
    desc_stats = numeric_df_subset.describe().to_dict()

    for feature in numeric_features:
        if feature not in df.columns:
            continue

        metadata = {
            'feature_name': feature,
            'data_type': column_info.get(feature, str(df[feature].dtype)),
            'description': generate_business_description(feature, column_info.get(feature, str(df[feature].dtype))),
            'null_count': df[feature].isna().sum(),
            'unique_count': df[feature].nunique()
        }

        if feature in desc_stats:
            stats = desc_stats[feature]
            metadata.update({
                'count': stats.get('count', 0),
                'mean': stats.get('mean', np.nan),
                'std': stats.get('std', np.nan),
                'min': stats.get('min', np.nan),
                '25%': stats.get('25%', np.nan),
                '50%': stats.get('50%', np.nan),
                '75%': stats.get('75%', np.nan),
                'max': stats.get('max', np.nan)
            })

        metadata_list.append(metadata)

    if not metadata_list:
        return pd.DataFrame(columns=['feature_name', 'data_type', 'description', 'null_count', 
                                    'unique_count', 'count', 'mean', 'std', 'min', 
                                    '25%', '50%', '75%', 'max'])

    return pd.DataFrame(metadata_list)

def compute_categorical_metadata(df, categorical_features, column_info):
    """Compute comprehensive metadata for categorical features."""
    metadata_list = []

    for feature in categorical_features:
        if feature not in df.columns:
            continue

        metadata = {
            'feature_name': feature,
            'data_type': column_info.get(feature, str(df[feature].dtype)),
            'description': generate_business_description(feature, column_info.get(feature, str(df[feature].dtype))),
            'null_count': df[feature].isna().sum(),
            'unique_count': df[feature].nunique()
        }

        if df[feature].dtype == 'object':
            value_counts = df[feature].value_counts().to_dict()
            if len(value_counts) > 10:
                top_10 = dict(list(value_counts.items())[:10])
                metadata['other_categories_count'] = len(value_counts) - 10
            else:
                metadata['other_categories_count'] = 0
        else:
            if not df[feature].isna().all():
                metadata['min_value'] = df[feature].min()
                metadata['max_value'] = df[feature].max()
                if pd.api.types.is_datetime64_any_dtype(df[feature]):
                    metadata['date_range_days'] = (df[feature].max() - df[feature].min()).days if pd.notna(df[feature].min()) else np.nan
                else:
                    metadata['value_range'] = float(df[feature].max() - df[feature].min()) if pd.notna(df[feature].min()) else np.nan

        metadata_list.append(metadata)

    if not metadata_list:
        return pd.DataFrame(columns=['feature_name', 'data_type', 'description',    'null_count', 'unique_count', 'min_value', 'max_value'])

    return pd.DataFrame(metadata_list)

def compute_identifier_metadata(df, identifier_features, column_info):
    """Compute comprehensive metadata for identifier features."""
    metadata_list = []

    for feature in identifier_features:
        if feature not in df.columns:
            continue

        metadata = {
            'feature_name': feature,
            'data_type': column_info.get(feature, str(df[feature].dtype)),
            'description': generate_business_description(feature, column_info.get(feature, str(df[feature].dtype))),
            'null_count': df[feature].isna().sum(),
            'unique_count': df[feature].nunique(),
            'total_count': len(df),
            'uniqueness_ratio': df[feature].nunique() / len(df) if len(df) > 0 else 0
        }

        duplicate_count = df[feature].duplicated().sum()
        metadata['duplicate_count'] = duplicate_count
        metadata['is_primary_key'] = duplicate_count == 0 and metadata['null_count'] == 0

        metadata_list.append(metadata)

    if not metadata_list:
        return pd.DataFrame(columns=['feature_name', 'data_type', 'description', 'null_count', 
                                    'unique_count', 'total_count', 'uniqueness_ratio', 
                                    'duplicate_count', 'is_primary_key'])

    return pd.DataFrame(metadata_list)

def export_data_dictionaries(numeric_df, categorical_df, identifier_df, output_base_path):
    """Export data dictionaries as CSV files to a specified base path."""
    output_base_path.mkdir(parents=True, exist_ok=True)

    csv_files = [
        (numeric_df, "numeric_data_dictionary.csv"),
        (categorical_df, "categorical_data_dictionary.csv"),
        (identifier_df, "identifier_data_dictionary.csv")
    ]

    for df_data, filename in csv_files:
        file_path = output_base_path / filename
        df_data.to_csv(file_path, index=False)

    return output_base_path

# --- Main Pipeline Function ---

def run_data_dictionary_pipeline(df: pd.DataFrame, output_dir_name: str = "data_dictionaries"):
    """
    Runs the data dictionary generation pipeline.

    Args:
        df (pd.DataFrame): The input DataFrame.
        output_dir_name (str): The name of the directory to save the data dictionaries.
                                This directory will be created relative to the project root.
    Returns:
        Path: The path to the directory where data dictionaries were exported.
    """
    column_info = {col: str(df[col].dtype) for col in df.columns}

    numeric_features, categorical_features, identifier_features = partition_features(column_info)

    numeric_df = compute_numeric_metadata(df, numeric_features, column_info)
    categorical_df = compute_categorical_metadata(df, categorical_features, column_info)
    identifier_df = compute_identifier_metadata(df, identifier_features, column_info)

    # Determine project root dynamically relative to this script's location
    # Assuming this utility is in 'project_root/notebooks/to_be_deleted/'
    # Adjust parents[] based on actual depth: 0=current, 1=parent, 2=grandparent, etc.
    # Here, it's 3 levels up from 'notebooks/to_be_deleted/' to 'bank-fraud-detection-project/'
    project_root = Path(__file__).resolve().parents[2]
    output_path = project_root / output_dir_name

    exported_path = export_data_dictionaries(numeric_df, categorical_df, identifier_df, output_path)

    return exported_path
