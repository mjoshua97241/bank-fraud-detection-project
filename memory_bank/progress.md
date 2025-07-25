# Progress

## What works

*   Project structure is set up according to Cookiecutter Data Science template.
*   Basic path management in `bank_fraud/config.py` is established.
*   Data dictionary generation utility (`data_dictionary_generator.py`) is functional.
*   Jupyter Notebook for initial data exploration (`1.0-mjv-initial-data-exploration.ipynb`) is set up, with zero-imputation preceding data dictionary generation.
*   Memory Bank directory and all core files (`projectbrief.md`, `productContext.md`, `activeContext.md`, `systemPatterns.md`, `techContext.md`, `progress.md`) are created.
*   `eda_checklist.md` has been moved to `notebooks/to_be_deleted/`.
*   Agent persona (expert data scientist) has been configured in `.cursorrules`.
*   New Jupyter Notebook workflow adopted: read `.ipynb`, edit `.py`.

## What's left to build

*   Populate data directories with actual data (if not already done).
*   Implement data ingestion and cleaning scripts.
*   Develop feature engineering pipelines.
*   Train and evaluate machine learning models.
*   Develop reporting and visualization components.
*   (Add more specific tasks as the project progresses)

## Current status

*   **Setup Phase:** Core project structure, documentation, and agent configuration are in place.
*   **Data Understanding:** Focus is currently on understanding the raw data through data dictionaries, initial exploration, and survival days analysis/visualization. Preparing for data filtering.

## Known issues

*   Initial `mkdir` command failed on Windows (resolved by implicit directory creation with `write_file`).
*   Discrepancy between `config.py`'s `DATA_DICTIONARIES_DIR` and actual file placement (resolved by adjusting `config.py`).
*   Persistent issues with direct file deletion commands on Windows (resolved by manual deletion).
*   (Document any ongoing issues or bugs here)
