# Contributing to This Project

Thank you for your interest in contributing! This document outlines the recommended development workflow to ensure consistency and quality. This project follows the principles of the [Cookiecutter Data Science](https://cookiecutter-data-science.drivendata.org/) template.

## Getting Started

### 1. Set Up the Environment

First, create the Conda environment using the `Makefile`. This will set up the correct Python version and all necessary dependencies from the `environment.yml` file.

```bash
make create_environment
```

After creation, activate the environment:

```bash
conda activate bank-fraud-detection-project
```

### 2. Install Dependencies

If the dependencies in `environment.yml` change, you can update your environment at any time by running:

```bash
make requirements
```

## Development Workflow

### 1. Create a New Branch

All new work, including notebooks for exploration or new features, should be done in a separate Git branch.

```bash
git checkout -b <your-branch-name>
```

A good branch name is descriptive, such as `feature/add-new-visualization` or `explore/initial-data-analysis`.

### 2. Data Handling

- **Raw Data:** Place raw, immutable data files in the `data/raw/` directory.
- **Data Processing:** Scripts used to process raw data and create feature sets should be located in `bank_fraud/`. These scripts should read from `data/raw/` or `data/interim/` and write their outputs to `data/processed/`. Use the `make data` command to run the main data processing script.

### 3. Notebooks vs. Modules

This project uses a clear separation between notebooks for exploration and Python modules for reusable code.

- **Notebooks (`notebooks/`):** Use Jupyter notebooks for initial data exploration, experimentation, and visualization.
  - **Naming Convention:** Follow the convention `number-initials-short-description.ipynb` (e.g., `1.0-mjv-initial-data-exploration.ipynb`).
  - **`%autoreload`:** At the top of your notebook, use the `autoreload` magic command. This ensures that any changes you make to the Python modules in `bank_fraud/` are automatically loaded into the notebook without needing to restart the kernel.

    ```python
    %load_ext autoreload
    %autoreload 2
    ```

- **Modules (`bank_fraud/`):** As you develop functions or classes in your notebooks that you intend to reuse, refactor them into Python modules within the `bank_fraud/` directory. This keeps the code organized, testable, and easy to import into other notebooks or scripts.

### 4. Code Style and Linting

This project uses `ruff` for linting and code formatting to maintain a consistent style.

- **To check for linting errors:**

  ```bash
  make lint
  ```

- **To automatically fix errors and format the code:**

  ```bash
  make format
  ```

### 5. Committing and Code Review

- **Commit Messages:** Write clear and concise commit messages that explain the "why" behind your changes.
- **Code Review:** When your work is complete, push your branch to the remote repository and open a pull request.
- **`nbautoexport` (Recommended):** For easier code reviews of notebooks, consider using a tool like `nbautoexport`, which automatically saves a `.py` version of your notebook on every save. Reviewing `.py` files is much easier than reviewing `.ipynb` files on platforms like GitHub.

By following these guidelines, you can help maintain the quality and consistency of the project.
