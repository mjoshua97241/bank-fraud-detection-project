# Project Plan

This document outlines the plan for the bank fraud detection project.

## Phase 1: Data Ingestion and Anonymization

- [X] Ingest raw data.
- [X] Anonymize sensitive columns.
- [X] Save processed data to `data/interim`.

## Phase 2: Data Preparation

- [X] Perform data cleaning and filtering.
- [X] Handle missing values.
- [X] Save prepared data to `data/processed`.

## Phase 3: Feature Selection and EDA

- [X] Conduct Information Value (IV) and correlation analysis.
- [X] Select the most predictive features.
- [X] Perform Exploratory Data Analysis (EDA) on the selected features.
- [X] Save the final feature set to `data/interim`.

## Phase 4: Final Feature EDA

- [X] Generate and analyze distribution plots for all final features.
- [X] Synthesize key insights and fraud patterns from the visualizations.

## Phase 5: Model Training, Evaluation, and Business Simulation

**Objective:** To develop, tune, and evaluate a machine learning model for fraud detection, and to translate its output into a cost-sensitive, actionable business decision framework.

**File:** `5.0-mjv-model-training-and-evaluation.ipynb` (and its corresponding `.py` script).

**Plan:**

1.  **Setup and Data Preparation:**
    *   Load the final processed dataset (`3.0_selected_features.parquet`).
    *   Identify and separate numerical and categorical features based on our `FEATURE_CATEGORIES` dictionary.
    *   Split the data into **training, validation, and holdout sets** using a stratified split to maintain the fraud ratio across all sets. This establishes our foundation for robust evaluation.

2.  **Preprocessing Pipeline Construction:**
    *   Create a `ColumnTransformer`-based preprocessing pipeline.
    *   This pipeline will apply `StandardScaler` to all numerical features and `OneHotEncoder` (with `handle_unknown='ignore'`) to all categorical features.
    *   This single pipeline object will be used throughout, ensuring we **fit only on the training data** and transform all three datasets consistently.

3.  **Model Training and Hyperparameter Tuning (Gate A & B Models):**
    *   We will focus directly on the `XGBoost` classifier, as established in your analysis.
    *   **Gate A Model (Precision-Tuned):**
        *   Create a full `Pipeline` that includes our preprocessor and the XGBoost classifier.
        *   Define a hyperparameter grid for `GridSearchCV`.
        *   Perform the grid search on the **training data**, using `scoring='precision'` to find the best parameters for the auto-blocking model.
        *   Save the best resulting model as `block_model.pkl`.
    *   **Gate B Model (AUC-PR-Tuned):**
        *   Create a second, similar `Pipeline`.
        *   Perform another `GridSearchCV` on the **training data**, but this time using `scoring='average_precision'` to find the best parameters for the analyst review queue model.
        *   Save this best model as `review_model_aucp.pkl`.

4.  **Business Simulation and Evaluation on Holdout Set:**
    *   Load the two saved models (`block_model.pkl` and `review_model_aucp.pkl`).
    *   **All analysis in this step will use the unseen holdout set.**
    *   **Gate A Analysis (Auto-Blocking):**
        *   Predict probabilities on the holdout set with the `block_model`.
        *   Conduct a threshold sweep analysis to create a table showing the trade-offs between `precision`, `alerts/day`, `FP/day`, and `Cost_FP/day`.
    *   **Gate B Analysis (Analyst Review Queue):**
        *   Predict probabilities on the holdout set with the `review_model_aucp`.
        *   Conduct a review capacity (`k`) analysis to create a table showing the trade-offs between `Precision@k`, `Recall@k`, `TP/day`, `FP/day`, `FN/day`, and the total daily costs (including review effort and missed fraud).

5.  **Fraud Risk Action Matrix:**
    *   Using the scores from the Gate B model and an important business feature (e.g., `max_txn_amt_day`), create the final 2D risk matrix.
    *   Define score and impact bins.
    *   Visualize the matrix and document the final decision rules (Block, Review, Pass).

6.  **Documentation and Finalization:**
    *   Throughout the script, add clear markdown explanations for each step, mirroring the clarity of your original notebooks.
    *   Conclude with a summary of the recommended `threshold` for Gate A and `k` for Gate B, and present the final Risk Action Matrix.