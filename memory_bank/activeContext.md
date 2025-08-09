# Active Context

## Current work focus

*   **Phase 6: Network Analysis of Fraudulent Transactions.**

## Recent changes

*   **Initiated Network Analysis Phase:** Created the `6.0-mjv-network-analysis.ipynb` notebook and established the initial structure for data loading and preparation.
*   **Completed SHAP Analysis:** Performed a deep-dive SHAP analysis to interpret the behavior of both the Precision-Optimized and AUC-PR-Optimized models.
*   **Created Interpretation Report:** Consolidated the SHAP analysis into a dedicated report, `SHAP_Model_Interpretation.md`, located in `reports/model_evaluation/`.
*   **Finalized Modeling Notebook:** Cleaned up and added a final conclusion to the `5.0-mjv-model-training-and-evaluation.ipynb` notebook, directing readers to the new interpretation report.

## Next steps

*   **Load and Preprocess Network Data:** Load the transaction data from `df_network.csv`, parse dates, and clean column names.
*   **Build Interactive Marimo Tool:** Develop a reactive notebook using Marimo to serve as an interactive analysis tool.
*   **Implement Dynamic Filtering:** Add UI controls (sliders for amount, dropdowns for transaction type) to allow analysts to filter the network in real-time.
*   **Visualize Network Structure:** Render the graph using `pyvis`, with node size representing its degree (number of connections) to highlight network hubs.
*   **Add Analytical Overlays:** Incorporate community detection and centrality metrics to uncover suspicious clusters and influential nodes within the graph.

## Active decisions and considerations

*   Using a Markdown-based Memory Bank system for project context.
*   Ensuring consistent path management across the project.
*   Ensuring consistent application of the expert data scientist persona.
*   Using `nbconvert` for robust `.ipynb` file interaction.
*   **Reminder for IV Analysis:** Investigate 2815 `CONFIRMED_FRAUD` accounts with zero PESONET/INSTAPAY transactions during IV analysis to understand their fraud patterns.
*   **WoE and IV calculation for categorical features will use the `iv_calculation.py` script.**
*   **Numerical features will be binned using user-provided specific definitions before IV calculation.**
*   **Decision to pre-process numerical binning rules for optimization.**
*   **Modeling Preprocessing Strategy:** To prevent data leakage, preprocessing steps like one-hot encoding and standardization will be fitted *only* on the training data and then applied to transform the validation and holdout sets.**
