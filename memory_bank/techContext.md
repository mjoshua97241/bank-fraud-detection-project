# Tech Context

## Technologies used

*   **Python 3.x:** Programming language.
*   **Conda/Mamba:** For environment management (via `environment.yml`).
*   **Pandas:** Data manipulation and analysis.
*   **NumPy:** Numerical operations.
*   **Scikit-learn:** Machine learning (expected).
*   **XGBoost/LightGBM (TBD):** Gradient boosting frameworks (expected).
*   **Jupyter:** Interactive development environment.
*   **MkDocs:** For project documentation (in `docs/`).
*   **Ruff:** Python linter/formatter (configured in `pyproject.toml`).
*   **Git:** Version control.

## Development setup

*   **Environment:** Managed by `environment.yml` (Conda/Mamba).
*   **Dependencies:** Installed via `conda env create -f environment.yml`.
*   **Code Editor:** (e.g., VS Code, PyCharm - user preference).
*   **Project Root:** `bank-fraud-detection-project/` (the inner one).

## Technical constraints

*   **Data Volume:** Potentially large datasets requiring efficient processing.
*   **Performance:** Fraud detection often requires near real-time processing.
*   **Interpretability:** Models may need to be interpretable for regulatory compliance and fraud analyst understanding.
*   **Scalability:** Solution should be scalable to handle growing transaction volumes.

## Dependencies

*   Refer to `environment.yml` for a comprehensive list of project dependencies.
*   (Add any specific external service dependencies here, e.g., database connections, APIs)
