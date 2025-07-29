# Progress

## What works

*   Project structure is set up according to Cookiecutter Data Science template.
*   Basic path management in `bank_fraud/config.py` is established.
*   Data dictionary generation utility (`data_dictionary_generator.py`) is functional.
*   Initial data exploration (`1.0-mjv-initial-data-exploration.py`) is set up, including zero-imputation, data dictionary generation, and **robust IV calculation for categorical and numerical features (with rounding for readability).**
*   **Dropped 30 columns based on IV calculation and feature selection criteria.**
*   Memory Bank directory and all core files (`projectbrief.md`, `productContext.md`, `activeContext.md`, `systemPatterns.md`, `techContext.md`, `progress.md`) are created.
*   `eda_checklist.md` has been moved to `notebooks/to_be_deleted/`.
*   Agent persona (expert data scientist) has been configured in `.cursorrules`.
*   New Jupyter Notebook workflow adopted: read `.ipynb`, edit `.py`.
*   **Numerical binning rules have been pre-processed and saved to `numerical_binning_rules_processed.csv` for optimized IV calculation.**
*   **Pre-processed numerical binning rules have been successfully integrated into `1.0-mjv-initial-data-exploration.py`, optimizing numerical IV calculation and addressing binning issues.**
*   **Updated IV interpretation and reasons in the Markdown table and `get_predictive_power` functions in `1.0-mjv-initial-data-exploration.py`.**

## What's left to build

*   Populate data directories with actual data (if not already done).
*   Implement data ingestion and cleaning scripts.
*   Develop feature engineering pipelines.
*   **Completed correlation analysis for categorical and numerical features, dropped highly correlated numerical features, and refined the analysis and decision section by removing redundant information.**
*   Perform EDA for final features, including bar graphs and fraud-related interpretations for Profile Traits, Transaction Size and Frequency, Network Behaviors, Time-Based Behaviors, and Fund Flow Patterns.
*   Train and evaluate machine learning models.
*   Develop reporting and visualization components.
*   (Add more specific tasks as the project progresses)

## Current status

*   **Setup Phase:** Core project structure, documentation, and agent configuration are in place.
*   **Data Understanding:** Focus is currently on understanding the raw data through data dictionaries, initial exploration, and survival days analysis/visualization. **Data filtering completed.**
*   **Visualization Refinement:** Ongoing efforts to improve clarity and adherence to data storytelling principles in visualizations (e.g., `dna_final_tag` distribution, survival days buckets).
*   **Binning Optimization:** Pre-processing of numerical binning rules is complete and integrated into the IV calculation.

## Known issues

*   Initial `mkdir` command failed on Windows (resolved by implicit directory creation with `write_file`).
*   Discrepancy between `config.py`'s `DATA_DICTIONARIES_DIR` and actual file placement (resolved by adjusting `config.py`).
*   Persistent issues with direct file deletion commands on Windows (resolved by manual deletion).
*   (Document any ongoing issues or bugs here)
