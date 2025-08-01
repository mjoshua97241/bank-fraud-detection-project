# System Patterns

## System architecture

*   **Cookiecutter Data Science Template:** Project structure follows this template for organization.
*   **Modular Python Code:** Core logic is encapsulated in the `bank_fraud/` package.
*   **Jupyter Notebooks:** Used for exploratory data analysis, prototyping, and model development.
*   **Data Versioning:** Data is organized into `raw`, `interim`, `processed`, and `external` stages.

## Key technical decisions

*   **Python:** Primary programming language.
*   **Pandas/NumPy:** For data manipulation and numerical operations.
*   **Scikit-learn/XGBoost (TBD):** For machine learning model development.
*   **Pathlib:** For robust path management.

## Design patterns in use

*   **Configuration-driven development:** Centralized configuration in `bank_fraud/config.py`.
*   **Modular functions:** Breaking down complex tasks into smaller, reusable functions (e.g., in `bank_fraud/features.py`, `bank_fraud/plots.py`).
*   **Data Dictionary Generation:** Automated metadata generation for features.
*   **Data Visualization:** Apply principles from Cole Nussbaumer Knaflic's "Storytelling with Data" to create clear, concise, and impactful visualizations, with particular attention to the effective and intentional use of color palettes. (Refer to `memory_bank/storytelling_with_data_principles.md` for detailed principles).
*   **Custom Color Palette:** Utilize a predefined custom color palette for all visualizations to ensure consistency and adherence to branding/aesthetic guidelines.
*   **Markdown in Python Scripts:** Use triple double-quoted strings (`"""..."""`) for multi-line Markdown explanations within Python scripts to facilitate easy copy-pasting.

## Cookiecutter Data Science Workflow

*   **Makefile:** Use the Makefile for automating tasks such as data processing, model training, and environment setup.
*   **Branching Strategy:** Create a new git branch for each new feature or experiment to maintain a clean and organized codebase.
*   **Data Ingestion & Anonymization (`1.0-mjv-data-ingestion-and-anonymization.py`):** Reads raw data from `data/raw`, performs initial cleaning and anonymization (e.g., hashing identifiers), and saves the interim dataset to `data/interim`.
*   **Data Preparation (`2.0-mjv-data-preparation.py`):** Reads interim data from `data/interim`, performs missing value imputation, feature engineering (e.g., `survival_days`), and data filtering, saving the prepared dataset to `data/processed`.
*   **Feature Selection & EDA (`3.0-mjv-feature-selection-and-eda.py`):** Reads prepared data from `data/processed`, conducts IV and correlation analysis, drops features, and performs initial EDA on the final feature set, saving the model-ready dataset to `data/processed`.
*   **Notebooks for Exploration:** Use Jupyter notebooks in the `notebooks` directory for exploratory data analysis and prototyping. Refactor any reusable code into Python modules in the `src` directory.
*   **Autoreload in Notebooks:** Use the `%autoreload` magic command in notebooks to automatically reload modules as they are updated.
*   **Code Reviews:** For code reviews, commit both the `.ipynb` notebook file and an exported `.py` script to ensure that the code can be reviewed without needing to run the notebook.
*   **Jupyter Notebook Workflow:**
    *   **Reading:** Read `.ipynb` files directly to understand their content.
    *   **Editing/Writing:** Only modify the `.py` version of the notebook, which are stored in `notebooks/to_be_deleted/py_version/`. The user will manually copy the content from these `.py` files to update the `.ipynb` files.

## Data Handling Strategies

*   **"Meaningful Zeros" (Absence of Activity/Occurrence):**
    *   **Description:** When a missing value logically signifies "zero activity," "zero amount," or "did not occur" for that specific feature (e.g., transaction counts, amounts, velocities, flags where `NaN` means the event simply didn't happen).
    *   **Treatment:** Impute with `0` (zero). This transforms the "absence of data" into "data indicating absence."
    *   **Timing:** This imputation is performed *before* data dictionary generation to ensure accurate representation.

*   **"Direct Imputation with Descriptive Strings" (Categorical/Object Type):**
    *   **Description:** When a missing value in a categorical or object column means "this event/attribute did not occur" or "is not applicable," and can be clearly described with a string (e.g., "No Interaction", "No Ticket").
    *   **Treatment:** Impute directly with a descriptive string (e.g., `'No Kiosk Interaction'`, `'No Ticket'`). This avoids creating an additional indicator column and makes the data more interpretable.
    *   **Timing:** This imputation is performed *before* data dictionary generation to ensure accurate representation.

*   **"Not Applicable" or "Unknown" (Non-Semantic Missingness - for Numerical/Datetime):**
    *   **Description:** When a missing value doesn't logically mean zero, but rather that the data point is genuinely unknown, not relevant, or simply wasn't recorded (e.g., `date_tagged` if an account was never restricted, `rank` if not applicable).
    *   **Treatment Options (chosen based on IV, domain, and model capability):**
        *   **Create Indicator Variables:** Introduce a new binary feature (e.g., `feature_name_is_missing`) that flags the presence of the original missingness. This allows the model to learn from the fact that the value was missing.
        *   **Impute Original Column:**
            *   For `datetime` columns: Leave `NaN` values as they are (models like XGBoost can handle them directly), as creating a placeholder can introduce artificial patterns.
            *   For `float64` columns: Impute `NaN` values with `0` (zero).
        *   **Drop the Feature:** If the feature has very high missingness (e.g., >90%) and low predictive power (low IV), it might be a candidate for removal.
    *   **Key Principle:** The decision is always feature-specific and informed by domain knowledge, Information Value (IV), and the modeling strategy.

*   **Conditional Filtering by Survival Days:**
    *   **Description:** Filtering the dataset based on `survival_days` to define the target population for "early fraud detection."
    *   **Treatment:**
        *   For `CONFIRMED_FRAUD` accounts: Only accounts with `survival_days > 7` days are retained. This ensures sufficient behavioral data for modeling.
        *   For `NON_FRAUD` accounts: Only accounts with `survival_days <= 60` days are retained. This prevents model bias where longer survival might incorrectly imply non-fraudulence.
        *   Accounts with `survival_days` between 0-7 days are excluded for both fraud and non-fraud, as they typically lack sufficient behavioral data for modeling.
    *   **Timing:** Applied after initial zero-imputation and direct categorical imputation, but before further EDA or IV calculations, to ensure all subsequent analysis is on the correct, unbiased population.

*   **Target Variable Transformation (`dna_final_tag` to `fraud_status`):**
    *   **Description:** The categorical target variable `dna_final_tag` is converted into a binary numerical format (`fraud_status`) to make it suitable for machine learning algorithms.
    *   **Treatment:**
        *   `CONFIRMED_FRAUD` is mapped to `1`.
        *   `NON_FRAUD` is mapped to `0`.
    *   **Timing:** This transformation is performed just before calculating Information Value (IV) and other statistical measures that require a numeric target.

## Component relationships

*   `bank_fraud/config.py`: Provides global configurations and paths to other modules.
*   `bank_fraud/dataset.py`: Handles data loading and initial processing.
*   `bank_fraud/features.py`: Contains logic for feature engineering, dependent on raw/interim data.
*   `bank_fraud/modeling/train.py` & `predict.py`: Utilize features and configurations for model operations.
*   `notebooks/`: Interact with `bank_fraud/` modules for analysis and development.
*   **`bank_fraud/utils/numerical_binning_definitions.py`:** New module containing pre-parsed numerical binning rules for optimized IV calculation.
*   **Refined Numerical Binning:** Implemented consistent and interpretable binning strategies for numerical features, including fixed-width bins for continuous variables, discrete bins for occurrence counts, and value-based bins for monetary amounts and ratios, with appropriate labeling (e.g., peso signs, percentages).

## Modeling Preprocessing Strategy

*   **Data Splitting:** The dataset will be split into three distinct sets: training, validation, and holdout, to ensure robust model development and unbiased evaluation.
*   **Preventing Data Leakage:** Preprocessing transformers (e.g., `StandardScaler` for numerical features, `OneHotEncoder` for categorical features) must be handled carefully to prevent data leakage.
    *   **Fit on Train Only:** The `.fit()` method for any preprocessor must be called *only* on the training dataset. This learns the scaling parameters or encoding mapping from the training data alone.
    *   **Transform All Sets:** The same fitted preprocessor is then used to `.transform()` the training, validation, and holdout datasets. This ensures that the same transformation logic is applied consistently across all data splits.
*   **Pipeline Integration:** These steps should be performed within the modeling script/notebook (e.g., `5.0-mjv-model-training-and-evaluation.ipynb`) after the initial data split.
*   **Resampling Strategy (Iterative Evaluation):**
    *   **Initial Focus:** We prioritize a core set of widely-used resampling techniques (`RandomOverSampler`, `SMOTE`, `RandomUnderSampler`) for initial evaluation. This allows for a rapid assessment of whether resampling generally benefits model performance and which direction (over- or under-sampling) is more promising.
    *   **Computational Efficiency:** This focused approach manages computational overhead, as evaluating every possible resampling technique with every baseline model can be time-consuming.
    *   **Data-Driven Expansion:** Further exploration of more advanced or specialized resampling methods will only occur if the initial evaluation demonstrates significant potential for improvement, ensuring resources are allocated effectively.
