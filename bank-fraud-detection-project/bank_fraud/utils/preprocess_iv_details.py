import pandas as pd
from pathlib import Path
import sys
import io

# Add project root to sys.path to allow imports from bank_fraud
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

from bank_fraud.config import REFERENCES_DIR

def parse_and_save_to_excel(file_path, writer, file_type):
    """
    Parses the custom block-based IV details file format and writes each feature to a separate sheet in an Excel file.
    """
    with open(file_path, 'r') as f:
        content = f.read()
        # Split by double newline, and filter out any empty blocks
        blocks = [b.strip() for b in content.split('\n\n') if b.strip()]

    print(f"Processing {len(blocks)} feature blocks from {file_path.name}...")

    for block in blocks:
        lines = block.split('\n')
        header_line = lines[0]
        
        # The feature name is the first item in the header
        feature_name = header_line.split('\t')[0]
        
        # The rest of the header
        header = header_line.split('\t')
        
        data_lines = lines[1:]
        
        # Skip empty blocks
        if not data_lines:
            continue
            
        # Reconstruct the block as a string for pandas to read
        data_io = io.StringIO('\n'.join(data_lines))
        
        # Read the data part of the block
        df_block = pd.read_csv(data_io, sep='\t', header=None, names=header, na_values=['-'])
        
        # The first column of the data is the 'Category'
        df_block.rename(columns={feature_name: 'Category'}, inplace=True)
        
        # Convert relevant columns to numeric, coercing errors
        for col in ['IV', 'PercentBad', 'PercentGood']:
            if col in df_block.columns:
                if col == 'IV':
                    df_block[col] = pd.to_numeric(df_block[col], errors='coerce').abs()
                else:
                    df_block[col] = pd.to_numeric(df_block[col], errors='coerce')

        # Write to a sheet named after the feature
        # Truncate sheet names to 31 characters, which is Excel's limit
        safe_sheet_name = feature_name[:31]
        df_block.to_excel(writer, sheet_name=safe_sheet_name, index=False)
        print(f"  - Saved feature '{feature_name}' to sheet '{safe_sheet_name}'")

def main():
    """
    Main function to execute the preprocessing.
    """
    categorical_file = REFERENCES_DIR / 'categorical_iv_details.csv'
    numerical_file = REFERENCES_DIR / 'numerical_iv_details.csv'
    output_excel_file = REFERENCES_DIR / 'iv_details_processed.xlsx'

    with pd.ExcelWriter(output_excel_file, engine='openpyxl') as writer:
        print(f"Creating processed Excel file at: {output_excel_file}")
        parse_and_save_to_excel(categorical_file, writer, 'Categorical')
        parse_and_save_to_excel(numerical_file, writer, 'Numerical')

    print("\nProcessing complete.")

if __name__ == "__main__":
    main()