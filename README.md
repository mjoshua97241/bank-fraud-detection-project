# Project Title: Risk Scoring and Network Mapping for Scalable Bank Fraud Detection

## Overview
This project developed a comprehensive and scalable bank fraud detection system designed to enhance the efficiency and accuracy of fraud identification. It integrates advanced analytical models with intuitive visualization tools to prioritize alerts and uncover complex fraud networks.

## Problem Statement
Traditional methods of bank fraud detection often struggle with scalability, efficiency in human review, and the ability to identify sophisticated, interconnected fraud rings. There was a critical need for a system that could effectively balance high precision in automated blocking with optimized human review processes.

## Solution Approach
The solution employs a dual-model approach:
1.  **Fraud Scorecard Model:** Utilizes machine learning to assign risk scores to transactions, enabling high-confidence auto-blocking and intelligent prioritization of alerts for human review.
2.  **Interactive Network Analysis Dashboard:** Visualizes relationships between accounts and transactions, allowing analysts to quickly identify and investigate complex fraud clusters that are difficult to detect manually.

## Key Features & Innovations
*   **Dual-Model Fraud Detection:** Engineered a system that improved analyst efficiency by an estimated 4x by auto-blocking high-confidence fraud with 94% precision and prioritizing alerts.
*   **Optimized Data Processing:** Processed and refined a large dataset (400MB, 1.2 million accounts), reducing the feature set from 154 to 65 through rigorous EDA and feature engineering, resulting in an optimized 30MB dataset for modeling.
*   **Advanced Predictive Modeling:** Developed and implemented a fraud scorecard model using various machine learning algorithms (including XGBoost) to achieve 94% precision for auto-blocking and enable flexible optimization of recall versus operational costs.
*   **Intuitive Network Visualization:** Designed and built an interactive network analysis dashboard with Cytoscape.js, significantly reducing analyst cognitive load and enabling the visualization of complex fraud rings beyond typical manual review limitations.
*   **Streamlined User Interface:** Developed a responsive and intuitive user interface using React and Tailwind CSS, consolidating data from 3 disparate systems into a single, unified dashboard to streamline analyst workflows.
*   **Enhanced Data Accessibility:** Integrated key UI components (lucide-react, react-datepicker, recharts) to facilitate data input, date range selection, and visual data representation, improving data accessibility and interpretability.
*   **Accelerated Onboarding:** Incorporated a guided tour with react-joyride to accelerate user onboarding, illustrating the intended end-to-end workflow.

## Technologies Utilized
*   **Data Processing & Modeling:** Python, Logistic Regression, Gaussian Naive Bayes, Decision Tree Classifier, XGBoost
*   **Frontend & Visualization:** React, Tailwind CSS, Cytoscape.js, lucide-react, react-datepicker, recharts, react-joyride

## Impact & Results
The system significantly improved fraud detection capabilities by:
*   Achieving an estimated 4x improvement in analyst efficiency.
*   Enabling 94% precision for auto-blocking high-confidence fraud.
*   Reducing analyst cognitive load through intuitive network visualization.
*   Consolidating data from multiple systems into a single, unified view.

## Live Demo
Explore the interactive web application showcasing the fraud analytics system:
[https://aegis-fraud-analytics-showcase-3c15grcq0-mjoshua97241s-projects.vercel.app/](https://aegis-fraud-analytics-showcase-3c15grcq0-mjoshua97241s-projects.vercel.app/)

## Confidentiality Notice
Due to the proprietary nature of the underlying dataset and specific implementation details, the project's code and raw data are confidential and cannot be publicly shared.

## Research Paper
A detailed research paper on this project is currently being prepared and will be linked here once published.

## Contact
*   LinkedIn: https://www.linkedin.com/in/mljosh/
*   GitHub: https://github.com/mjoshua97241