"""
Model training and evaluation module for the House Price Prediction project.
"""

import numpy as np
import pandas as pd
import joblib

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score, RandomizedSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_error

def train_linear_regression(X_train, y_train):
    """
    Train a linear regression model.
    
    Args:
        X_train (np.ndarray): Training features
        y_train (np.ndarray): Training labels
    
    Returns:
        LinearRegression: Trained model
    """
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

def train_decision_tree(X_train, y_train, max_depth=None, random_state=42):
    """
    Train a decision tree regression model.
    
    Args:
        X_train (np.ndarray): Training features
        y_train (np.ndarray): Training labels
        max_depth (int, optional): Maximum depth of the tree
        random_state (int): Random seed for reproducibility
    
    Returns:
        DecisionTreeRegressor: Trained model
    """
    model = DecisionTreeRegressor(max_depth=max_depth, random_state=random_state)
    model.fit(X_train, y_train)
    return model

def train_random_forest(X_train, y_train, n_estimators=100, random_state=42):
    """
    Train a random forest regression model.
    
    Args:
        X_train (np.ndarray): Training features
        y_train (np.ndarray): Training labels
        n_estimators (int): Number of trees in the forest
        random_state (int): Random seed for reproducibility
    
    Returns:
        RandomForestRegressor: Trained model
    """
    model = RandomForestRegressor(n_estimators=n_estimators, random_state=random_state)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X, y, model_name="Model"):
    """
    Evaluate a model on given data.
    
    Args:
        model: The trained model
        X (np.ndarray): Features
        y (np.ndarray): Labels
        model_name (str): Name of the model for display
    
    Returns:
        dict: Evaluation metrics
    """
    predictions = model.predict(X)
    mse = mean_squared_error(y, predictions)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y, predictions)
    
    print(f"{model_name} performance:")
    print(f"RMSE: {rmse:.2f}")
    print(f"MAE: {mae:.2f}")
    
    return {
        "model_name": model_name,
        "predictions": predictions,
        "mse": mse,
        "rmse": rmse,
        "mae": mae
    }

def cross_validate_model(model, X, y, cv=10, model_name="Model"):
    """
    Perform cross-validation for a model.
    
    Args:
        model: The model to validate
        X (np.ndarray): Features
        y (np.ndarray): Labels
        cv (int): Number of cross-validation folds
        model_name (str): Name of the model for display
    
    Returns:
        dict: Cross-validation scores
    """
    scores = cross_val_score(model, X, y, scoring="neg_mean_squared_error", cv=cv)
    rmse_scores = np.sqrt(-scores)
    
    print(f"{model_name} cross-validation:")
    print(f"RMSE scores: {rmse_scores}")
    print(f"Mean RMSE: {rmse_scores.mean():.2f}")
    print(f"Standard deviation: {rmse_scores.std():.2f}")
    
    return {
        "model_name": model_name,
        "rmse_scores": rmse_scores,
        "mean_rmse": rmse_scores.mean(),
        "std_rmse": rmse_scores.std()
    }

def tune_random_forest(X_train, y_train, cv=3, n_iter=10, random_state=42):
    """
    Tune hyperparameters for a random forest model.
    
    Args:
        X_train (np.ndarray): Training features
        y_train (np.ndarray): Training labels
        cv (int): Number of cross-validation folds
        n_iter (int): Number of parameter settings to try
        random_state (int): Random seed for reproducibility
    
    Returns:
        tuple: (best_model, best_params, best_score) - 
               Best model, its parameters, and score
    """
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_features': ['auto', 'sqrt', 'log2'],
        'max_depth': [10, 20, 30, None]
    }
    
    rnd_search = RandomizedSearchCV(
        RandomForestRegressor(random_state=random_state),
        param_distributions=param_grid,
        n_iter=n_iter,
        cv=cv,
        scoring='neg_mean_squared_error',
        random_state=random_state,
        n_jobs=-1
    )
    
    rnd_search.fit(X_train, y_train)
    
    best_model = rnd_search.best_estimator_
    best_params = rnd_search.best_params_
    best_score = np.sqrt(-rnd_search.best_score_)
    
    print("Best Parameters:", best_params)
    print(f"Best RMSE: {best_score:.2f}")
    
    return best_model, best_params, best_score

def save_model(model, filepath):
    """
    Save a trained model to disk.
    
    Args:
        model: The trained model
        filepath (str): Path where the model will be saved
    """
    joblib.dump(model, filepath)
    print(f"Model saved to {filepath}")

def load_model(filepath):
    """
    Load a trained model from disk.
    
    Args:
        filepath (str): Path where the model is saved
    
    Returns:
        The loaded model
    """
    model = joblib.load(filepath)
    print(f"Model loaded from {filepath}")
    return model

def feature_importance(model, feature_names):
    """
    Get feature importance from a model that supports it.
    
    Args:
        model: The trained model (must have feature_importances_ attribute)
        feature_names (list): Names of the features
    
    Returns:
        pd.Series: Feature importances sorted in descending order
    """
    if not hasattr(model, 'feature_importances_'):
        raise ValueError("Model does not have feature_importances_ attribute")
    
    importances = model.feature_importances_
    return pd.Series(importances, index=feature_names).sort_values(ascending=False)