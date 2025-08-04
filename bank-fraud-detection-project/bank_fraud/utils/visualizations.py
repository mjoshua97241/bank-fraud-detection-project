import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
import shap # For beeswarm plots

def plot_confusion_matrix(y_true, y_pred, model_name, save_path, project_root):
    """
    Generates and saves a styled confusion matrix plot.
    """
    cm = confusion_matrix(y_true, y_pred)
    
    # Create annotations with names and values
    group_names = ['True Neg', 'False Pos', 'False Neg', 'True Pos']
    group_counts = [f"{value:0.0f}" for value in cm.flatten()]
    group_percentages = [f"{value:.2%}" for value in cm.flatten() / np.sum(cm)]
    
    labels = [f"{v1}\n{v2}\n{v3}" for v1, v2, v3 in zip(group_names, group_counts, group_percentages)]
    labels = np.asarray(labels).reshape(2, 2)
    
    # Define the axis labels
    axis_labels = ['NON FRAUD', 'CONFIRMED FRAUD']

    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=labels, fmt='', cmap='Blues', cbar=False, 
                xticklabels=axis_labels, yticklabels=axis_labels,
                linewidths=1, linecolor='white')
    
    plt.title(f'Confusion Matrix: {model_name}\n', fontsize=16)
    plt.ylabel('Actual Label', fontsize=12)
    plt.xlabel('Predicted Label', fontsize=12)
    
    # Save the figure
    plt.savefig(save_path, bbox_inches='tight')
    print(f"Confusion matrix for {model_name} saved to: {save_path.relative_to(project_root)}")
    plt.show()

def plot_feature_importance(model, model_name, save_path, project_root, top_n=20, save_csv_path=None):
    """
    Generates and saves a styled feature importance plot for a pipeline model.
    """
    # Extract the preprocessor and classifier from the pipeline
    preprocessor = model.named_steps['preprocessor']
    classifier = model.named_steps['classifier']
    
    # Get feature names from the preprocessor
    try:
        feature_names = preprocessor.get_feature_names_out()
    except AttributeError:
        print("Warning: .get_feature_names_out() not available. Feature names might be less reliable.")
        return

    # Create a DataFrame for feature importances
    importances = classifier.feature_importances_
    feature_importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': importances
    }).sort_values(by='importance', ascending=False).head(top_n)
    
    plt.figure(figsize=(12, 8))
    sns.barplot(x='importance', y='feature', data=feature_importance_df, palette='viridis')
    
    plt.title(f'Top {top_n} Feature Importances: {model_name}\n', fontsize=16)
    plt.xlabel('Importance Score', fontsize=12)
    plt.ylabel('Feature', fontsize=12)
    plt.tight_layout()
    
    # Save the figure
    plt.savefig(save_path, bbox_inches='tight')
    print(f"Feature importance plot for {model_name} saved to: {save_path.relative_to(project_root)}")
    plt.show()

    if save_csv_path:
        feature_importance_df.to_csv(save_csv_path, index=False)
        print(f"Feature importance data for {model_name} saved to: {save_csv_path.relative_to(project_root)}")

def plot_beeswarm(model, X_data, model_name, save_path, project_root, top_n=20, save_csv_path=None):
    """
    Generates and saves a SHAP beeswarm plot and optionally saves SHAP values to a CSV.
    """
    # Extract the preprocessor and classifier from the pipeline
    preprocessor = model.named_steps['preprocessor']
    classifier = model.named_steps['classifier']

    # Transform X_data using the preprocessor
    X_data_preprocessed = preprocessor.transform(X_data)

    # Get feature names from the preprocessor
    try:
        feature_names = preprocessor.get_feature_names_out()
    except AttributeError:
        print("Warning: .get_feature_names_out() not available. SHAP plot feature names might be less reliable.")
        feature_names = [f"feature_{i}" for i in range(X_data_preprocessed.shape[1])]
    
    # Create a DataFrame with preprocessed data and feature names for SHAP
    X_data_preprocessed_df = pd.DataFrame(X_data_preprocessed, columns=feature_names)

    # Create a SHAP explainer
    explainer = shap.TreeExplainer(classifier)
    shap_values = explainer.shap_values(X_data_preprocessed_df)

    # Plot the SHAP beeswarm plot
    plt.figure(figsize=(12, 8))
    shap.summary_plot(shap_values, X_data_preprocessed_df, show=False, max_display=top_n)
    plt.title(f'SHAP Beeswarm Plot: {model_name}\n', fontsize=16)
    plt.tight_layout()

    # Save the figure
    plt.savefig(save_path, bbox_inches='tight')
    print(f"SHAP beeswarm plot for {model_name} saved to: {save_path.relative_to(project_root)}")
    plt.show()

    # Save SHAP values to CSV if a path is provided
    if save_csv_path:
        # Calculate mean absolute SHAP value for each feature
        mean_abs_shap = np.abs(shap_values).mean(axis=0)
        shap_importance_df = pd.DataFrame({
            'feature': feature_names,
            'mean_abs_shap_value': mean_abs_shap
        }).sort_values(by='mean_abs_shap_value', ascending=False)
        
        shap_importance_df.to_csv(save_csv_path, index=False)
        print(f"SHAP importance data for {model_name} saved to: {save_csv_path.relative_to(project_root)}")