# Initial Data Exploration (EDA) Checklist

This checklist provides a structured approach for conducting Exploratory Data Analysis (EDA) on a new dataset, particularly in a fraud detection context. Use this guide to ensure a thorough and consistent analysis.

---

### Phase 1: Basic Data Inspection & Setup
*Goal: Get a high-level overview of the dataset's structure and quality.*

- [ ] **Import Libraries:** Import `pandas`, `numpy`, `matplotlib`, `seaborn`, etc.
- [ ] **Load Data:** Read the raw data file (e.g., `pd.read_csv()`).
- [ ] **First Glance (`.head()`, `.tail()`):** Look at the first and last few rows to understand the columns and data format.
- [ ] **Dataset Shape (`.shape`):** How many rows (transactions) and columns (features) are there?
- [ ] **Data Types and Nulls (`.info()`):**
    -   Check the data type of each column. Are dates stored as objects? Are numbers stored as strings?
    -   Identify columns with missing values. How many are there?
- [ ] **Check for Duplicates (`.duplicated().sum()`):** Are there any duplicate rows in the dataset?
- [ ] **Descriptive Statistics (`.describe()`):** Get a summary of the central tendency, dispersion, and shape of the distribution for all numerical columns.

### Phase 2: Univariate Analysis (Analyzing Single Variables)
*Goal: Understand the distribution and characteristics of each individual feature.*

- [ ] **Target Variable Analysis (`isFraud`):**
    -   Calculate the frequency of fraudulent vs. non-fraudulent transactions (`.value_counts()`).
    -   Visualize the class distribution with a bar plot. *Expect a highly imbalanced dataset.*
- [ ] **Numerical Features:**
    -   Visualize distributions using histograms or KDE plots. Are they skewed, normal, or bimodal?
    -   Identify potential outliers using box plots.
- [ ] **Categorical Features:**
    -   Count the number of unique values in each column (`.nunique()`).
    -   Visualize the frequency of each category using bar plots (`.value_counts().plot(kind='bar')`).
- [ ] **Date/Time Features:**
    -   Convert date/time columns to the proper `datetime` data type.
    -   Extract useful components (e.g., hour of day, day of week, month).
    -   Plot transaction volume over time to identify trends, seasonality, or anomalies.

### Phase 3: Bivariate & Multivariate Analysis (Analyzing Relationships)
*Goal: Discover how features interact with each other and with the target variable.*

- [ ] **Correlation Analysis (Numerical Features):**
    -   Create a correlation matrix (`.corr()`).
    -   Visualize the matrix with a heatmap (`sns.heatmap()`) to quickly spot highly correlated features.
- [ ] **Relationship with Target Variable (`isFraud`):**
    -   **Numerical vs. Target:** Compare the distributions of numerical features for fraudulent and non-fraudulent transactions. (e.g., `sns.boxplot(x='isFraud', y='transactionAmount')`). Do fraudulent transactions tend to be larger or smaller?
    -   **Categorical vs. Target:** Analyze the fraud rate across different categories. (e.g., a grouped bar chart showing the fraud rate per device type).
- [ ] **Relationships Between Features:**
    -   Explore interactions between key features. For example, does the relationship between transaction amount and fraud risk change depending on the time of day?

### Phase 4: Summarize Findings & Propose Next Steps
*Goal: Document your findings and create a plan for the next stage.*

- [ ] **Summarize Key Findings:** Write down your main observations in a markdown cell.
- [ ] **Formulate Initial Hypotheses:** Based on your analysis, what are your initial ideas about what drives fraud?
- [ ] **Propose a Strategy:** Document your plan for handling missing values, outliers, and any data type corrections.
- [ ] **Plan for Feature Engineering:** List potential new features you could create.

---

### Next Steps: Data Cleaning & Feature Engineering

Once the EDA is complete and the plan is documented, the next step is to create a new notebook (e.g., `2.0-data-cleaning-and-feature-engineering.ipynb`). In this new notebook, you will execute the plan by:

1.  **Applying the data cleaning strategy** (handling nulls, outliers, etc.).
2.  **Creating the new features** you identified.
3.  **Saving the final, cleaned dataset** to the `data/processed` directory.
