import pandas as pd
from pathlib import Path

def mask_sensitive_iv_details(project_root: Path):
    """
    Masks sensitive category names in IV details CSV files.
    This script is intended to be run locally and should be in .gitignore.
    """
    iv_details_dir = project_root / 'references' / 'iv_details'

    # List of files to process
    files_to_mask = [
        'first_fila_bank_code_iv_details.csv',
        'first_kiosk_interaction_organisation_name_iv_details.csv',
        'first_kiosk_interaction_organisation_site_name_iv_details.csv',
        'latest_kiosk_interaction_organisation_name_iv_details.csv',
        'latest_kiosk_interaction_organisation_site_name_iv_details.csv',
        'orig_industry_iv_details.csv',
        'orig_occupation_iv_details.csv',
        'first_kiosk_interaction_organisation_presence_category_iv_details.csv',
        'latest_kiosk_interaction_organisation_presence_category_iv_details.csv',
    ]

    for filename in files_to_mask:
        file_path = iv_details_dir / filename
        if not file_path.exists():
            print(f"Warning: File not found: {file_path.relative_to(project_root)}")
            continue

        print(f"Processing {file_path.relative_to(project_root)}...")
        df = pd.read_csv(file_path)

        feature_name = filename.replace('_iv_details.csv', '')

        # Apply generic masking for all identified sensitive features
        if 'kiosk_interaction' in feature_name or 'organisation_name' in feature_name or 'organisation_site_name' in feature_name or 'bank_code' in feature_name or 'orig_industry' in feature_name or 'orig_occupation' in feature_name or 'organisation_presence_category' in feature_name:
            unique_categories = df['Category'].unique()
            masking_prefix = 'Site_' if 'site_name' in feature_name else \
                             ('Bank_' if 'bank_code' in feature_name else \
                             ('Industry_' if 'orig_industry' in feature_name else \
                             ('Occupation_' if 'orig_occupation' in feature_name else \
                             ('PresenceCat_' if 'organisation_presence_category' in feature_name else 'Org_'))))
            category_counter = 1
            dynamic_mask_map = {}
            for cat in unique_categories:
                # Exclude 'Grand Total' and 'No Kiosk Interaction' from generic masking
                if cat not in ['Grand Total', 'No Kiosk Interaction']:
                    dynamic_mask_map[cat] = f"{masking_prefix}{category_counter:02d}"
                    category_counter += 1
            df['Category'] = df['Category'].replace(dynamic_mask_map)

        df.to_csv(file_path, index=False)
        print(f"Masking complete for {file_path.relative_to(project_root)}")

if __name__ == "__main__":
    # Determine the project root dynamically
    # Assumes the script is run from the project root or a subdirectory
    current_dir = Path(__file__).parent
    project_root = current_dir
    while project_root.name != 'bank-fraud-detection-project':
        if project_root.parent == project_root: # Reached root directory
            raise Exception("Project root 'bank-fraud-detection-project' not found.")
        project_root = project_root.parent
    
    mask_sensitive_iv_details(project_root)