# bank-fraud-detection-project

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

This project developed a comprehensive and scalable bank fraud detection system, specifically focusing on an **early detection model** for **EFT (Electronic Funds Transfer) type transactions**. Leveraging an account dataset from **January 2025 to May 2025**, this system is designed to enhance the efficiency and accuracy of fraud identification. It integrates advanced analytical models with intuitive visualization tools to prioritize alerts and uncover complex fraud networks. This capstone project was developed in collaboration with a Data Scientist mentor from the financial industry, drawing insights from real-world banking challenges while focusing on a proof-of-concept for academic purposes.

## Project Organization

> **Note:** This project follows the [Cookiecutter Data Science](https://cookiecutter-data-science.drivendata.org/) template. The structure below is a standard guide; some files may be replaced by alternatives (e.g., `environment.yml` for `requirements.txt`) depending on the project's specific tooling.

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks, Marimo files. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`. These notebooks follow a structured EDA process, emphasizing robust data quality checks and feature selection using metrics like Information Value (IV).
│
├── pyproject.toml     <- Project configuration file with package metadata for bank_fraud
│                         and configuration for tools like ruff.
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│   └── iv_details     <- Individual CSV files containing detailed IV calculations for each feature.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment (this project uses environment.yml).
│
├── setup.cfg          <- Configuration file for flake8 (this project uses ruff, configured in pyproject.toml).
│
└── bank_fraud   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes bank_fraud a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    ├── modeling                
    │   ├── __init__.py 
    │   ├── predict.py          <- Code to run model inference with trained models          
    │   └── train.py            <- Code to train models
    │
    └── plots.py                <- Code to create visualizations
```

### Data Scope and Rationale

This project exclusively utilizes an account dataset from **January 2025 to May 2025**. This specific timeframe is chosen because fraud behaviors are constantly evolving. Focusing on recent data ensures our early detection model learns from the most relevant and up-to-date behavioral characteristics, as older datasets may not accurately reflect current fraud patterns.

--------

