"""
Visualization module for the House Price Prediction project.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

def plot_histogram(data, bins=50, figsize=(20, 15)):
    """
    Plot histograms of all numeric features.
    
    Args:
        data (pd.DataFrame): The data to visualize
        bins (int): Number of bins for histograms
        figsize (tuple): Figure size
    """
    data.hist(bins=bins, figsize=figsize)
    plt.tight_layout()
    plt.show()

def plot_scatter_map(data, s_size="population", c_var="median_house_value",
                     alpha=0.4, figsize=(10, 7)):
    """
    Create scatter plot showing geographic distribution with additional variables.
    
    Args:
        data (pd.DataFrame): The data to visualize
        s_size (str): Column name to use for point size
        c_var (str): Column name to use for point color
        alpha (float): Transparency of points
        figsize (tuple): Figure size
    """
    plt.figure(figsize=figsize)
    plt.scatter(data["longitude"], data["latitude"], 
                alpha=alpha,
                s=data[s_size]/100, 
                label=s_size,
                c=data[c_var], 
                cmap=plt.get_cmap("jet"))
    plt.colorbar(label=c_var)
    plt.legend()
    plt.title(f"Housing distribution by {s_size} and {c_var}")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.show()

def plot_correlation_matrix(data):
    """
    Plot correlation matrix of numeric features.
    
    Args:
        data (pd.DataFrame): The data to visualize
    """
    # Only select numeric columns for correlation
    corr = data.select_dtypes(include=[np.number]).corr()
    
    # Create mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))
    
    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(11, 9))
    
    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    
    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .5})
    plt.title("Feature Correlation Matrix")
    plt.show()

def plot_predictions_vs_actual(y_true, y_pred, title="Actual vs Predicted Values"):
    """
    Create scatter plot comparing actual values with model predictions.
    
    Args:
        y_true (np.ndarray): Actual values
        y_pred (np.ndarray): Predicted values
        title (str): Plot title
    """
    plt.figure(figsize=(6, 6))
    plt.scatter(y_true, y_pred, alpha=0.3)
    plt.xlabel("Actual Values")
    plt.ylabel("Predicted Values")
    plt.title(title)
    
    # Add perfect prediction line
    min_val = min(y_true.min(), y_pred.min())
    max_val = max(y_true.max(), y_pred.max())
    plt.plot([min_val, max_val], [min_val, max_val], 'r--')
    
    plt.tight_layout()
    plt.show()

def plot_feature_importance(importance_series, top_n=20, figsize=(12, 8)):
    """
    Plot feature importance.
    
    Args:
        importance_series (pd.Series): Series with feature names as index and importance as values
        top_n (int): Number of top features to display
        figsize (tuple): Figure size
    """
    plt.figure(figsize=figsize)
    
    # Get top features
    top_features = importance_series.head(top_n)
    
    # Create bar plot
    top_features.plot(kind='bar')
    plt.title(f"Top {top_n} Feature Importances")
    plt.xlabel("Features")
    plt.ylabel("Importance")
    plt.tight_layout()
    plt.show()

def plot_learning_curves(model, X_train, y_train, X_val, y_val, train_sizes=np.linspace(0.1, 1.0, 10)):
    """
    Plot learning curves for a model.
    
    Args:
        model: The model to evaluate
        X_train (np.ndarray): Training features
        y_train (np.ndarray): Training labels
        X_val (np.ndarray): Validation features
        y_val (np.ndarray): Validation labels
        train_sizes (np.ndarray): Array of training sizes to evaluate
    """
    from sklearn.model_selection import learning_curve
    
    train_sizes, train_scores, val_scores = learning_curve(
        model, X_train, y_train, train_sizes=train_sizes,
        scoring='neg_mean_squared_error', cv=5)
    
    train_rmse = np.sqrt(-train_scores.mean(axis=1))
    val_rmse = np.sqrt(-val_scores.mean(axis=1))
    
    plt.figure(figsize=(10, 6))
    plt.grid()
    plt.plot(train_sizes, train_rmse, 'o-', color='r', label='Training error')
    plt.plot(train_sizes, val_rmse, 'o-', color='g', label='Validation error')
    plt.legend(loc='best')
    plt.xlabel('Training examples')
    plt.ylabel('RMSE')
    plt.title('Learning Curves')
    plt.show()