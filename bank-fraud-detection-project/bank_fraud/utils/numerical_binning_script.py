import pandas as pd
import numpy as np
from pathlib import Path
import re

project_root = Path('E:/Personal/Full_Stack_Data_Analyst/Data_Science/GitHub/bank-fraud-detection-project/bank-fraud-detection-project')
rules_filepath = project_root / 'references' / 'numerical_binning_rules.csv'
output_filepath = project_root / 'bank_fraud' / 'utils' / 'numerical_binning_definitions.py'

def parse_shorthand_value(s_val: str) -> float:
    s_val = str(s_val).strip().upper()
    if 'M' in s_val:
        return float(s_val.replace('M', '')) * 1_000_000
    if 'K' in s_val:
        return float(s_val.replace('K', '')) * 1_000
    try:
        return float(s_val)
    except ValueError:
        return np.nan

def parse_bin_rule(rule_str: str) -> dict:
    rule_str = rule_str.strip()
    rule_lower = rule_str.lower()

    # Handle special text rules first
    if 'negative accel' in rule_lower:
        return {'type': 'text', 'label': rule_str, 'value': -np.inf} # Use -inf for comparison
    if 'positive accel' in rule_lower:
        return {'type': 'text', 'label': rule_str, 'value': np.inf} # Use +inf for comparison
    
    # Handle ranges
    if ' - <' in rule_str: # e.g., "0 - <5"
        parts = rule_str.split(' - <')
        low = parse_shorthand_value(parts[0])
        high = parse_shorthand_value(parts[1])
        return {'type': 'range_le_lt', 'low': low, 'high': high, 'label': rule_str}
    elif ' - ' in rule_str: # e.g., "0 - 5" (assuming inclusive lower, exclusive upper)
        parts = rule_str.split(' - ')
        low = parse_shorthand_value(parts[0])
        high = parse_shorthand_value(parts[1])
        return {'type': 'range_le_lt', 'low': low, 'high': high, 'label': rule_str}
    elif rule_str.endswith('+'): # e.g., "10+"
        low = parse_shorthand_value(rule_str.replace('+', ''))
        return {'type': 'range_ge', 'low': low, 'label': rule_str}
    elif rule_str.startswith('<'): # e.g., "<1K"
        high = parse_shorthand_value(rule_str.replace('<', ''))
        return {'type': 'range_lt', 'high': high, 'label': rule_str}
    elif rule_str.startswith('>='): # e.g., ">=10"
        low = parse_shorthand_value(rule_str.replace('>=', ''))
        return {'type': 'range_ge', 'low': low, 'label': rule_str}
    elif rule_str.startswith('>'): # e.g., ">10"
        low = parse_shorthand_value(rule_str.replace('>', ''))
        return {'type': 'range_gt', 'low': low, 'label': rule_str}
    
    # Handle exact numerical values
    try:
        val = parse_shorthand_value(rule_str)
        if not np.isnan(val):
            return {'type': 'exact', 'value': val, 'label': rule_str}
    except ValueError:
        pass

    return {'type': 'unhandled', 'label': rule_str} # Fallback for unhandled formats

# Load the original binning rules
try:
    binning_rules_df = pd.read_csv(rules_filepath, encoding='cp1252', sep='	') # Process all features
except FileNotFoundError:
    print(f"Error: Binning rules file not found at {rules_filepath}")
    exit()

BINNING_DEFINITIONS = {}
for index, row in binning_rules_df.iterrows():
    feature_name = row['feature']
    bin_edges_str = row['bin_edges']
    
    rules = [r.strip() for r in bin_edges_str.split(',')]
    parsed_rules = [parse_bin_rule(rule) for rule in rules]
    
    BINNING_DEFINITIONS[feature_name] = parsed_rules

# Write the dictionary to a Python file
with open(output_filepath, 'w') as f:
    f.write("BINNING_DEFINITIONS = {\n")
    for feature, rules_list in BINNING_DEFINITIONS.items():
        f.write(f"    '{feature}': [\n")
        for rule in rules_list:
            # Format float values to ensure they are written correctly (e.g., inf, -inf)
            formatted_rule = str(rule).replace('inf', 'float("inf")').replace('-inf', '-float("inf")')
            f.write(f"        {formatted_rule},\n")
        f.write(f"    ],\n")
    f.write("}\n")

print(f"Binning definitions saved to: {output_filepath.relative_to(project_root.parent)}")
