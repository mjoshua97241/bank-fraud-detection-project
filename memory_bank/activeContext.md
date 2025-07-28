# Active Context

## Current work focus

*   Integrating the Memory Bank system into the workflow.
*   Refining data dictionary generation and access.
*   Continuing initial data exploration in `1.0-mjv-initial-data-exploration.py`, including zero-imputation, data dictionary generation, **completed data filtering**, and IV calculation for categorical features.
*   Adopting a new Jupyter Notebook workflow: read `.ipynb`, edit `.py`.
*   **Completed and debugged IV and WoE calculation code for categorical and numerical features, ensuring robust column handling, consistent naming, and rounding to 2 decimal places for IV/WoE and 4 for percentages.**

## Recent changes

*   Corrected `PROJECT_ROOT` and `project_root` definitions in `bank_fraud/config.py` and `bank_fraud/utils/data_dictionary_generator.py`.
*   Adjusted `DATA_DICTIONARIES_DIR` in `bank_fraud/config.py` to point directly to `REFERENCES_DIR`.
*   Modified Jupyter Notebook print statement for `exported_path` to show relative path.
*   Created `data_dictionary_explanation.md` for Jupyter Notebook.
*   Moved `eda_checklist.md` to `notebooks/to_be_deleted/`.
*   Updated `.cursorrules` with agent persona.
*   **Created `iv_calculation.py` in `notebooks/to_be_deleted/` for categorical IV/WoE calculation.**

## Next steps

*   Continue initial data loading and exploration in `1.0-mjv-initial-data-exploration.ipynb`.
*   **Prepare for IV analysis of numerical features, where specific binning definitions will be provided by the user.**
*   **PRIORITY: Fix binning issues in numerical IV tables (e.g., 'Other' category, incorrect ranges).**

## Active decisions and considerations

*   Using a Markdown-based Memory Bank system for project context.
*   Ensuring consistent path management across the project.
*   Ensuring consistent application of the expert data scientist persona.
*   Using `nbconvert` for robust `.ipynb` file interaction.
*   **Reminder for IV Analysis:** Investigate 2815 `CONFIRMED_FRAUD` accounts with zero PESONET/INSTAPAY transactions during IV analysis to understand their fraud patterns.
*   **WoE and IV calculation for categorical features will use the `iv_calculation.py` script.**
*   **Numerical features will be binned using user-provided specific definitions before IV calculation.**
