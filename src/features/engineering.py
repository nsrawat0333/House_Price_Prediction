"""
Feature engineering module for the House Price Prediction project.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

def create_features(data):
    """
    Create additional features from existing ones.
    
    Args:
        data (pd.DataFrame): The housing data
    
    Returns:
        pd.DataFrame: Data with additional engineered features
    """
    result = data.copy()
    
    # Create bedrooms per household
    if "total_bedrooms" in result.columns and "households" in result.columns:
        result["bedrooms_per_household"] = result["total_bedrooms"] / result["households"]
    
    # Create population per household
    if "population" in result.columns and "households" in result.columns:
        result["population_per_household"] = result["population"] / result["households"]
    
    # Create rooms per household
    if "total_rooms" in result.columns and "households" in result.columns:
        result["rooms_per_household"] = result["total_rooms"] / result["households"]
    
    return result

def scale_features(train_data, test_data=None):
    """
    Scale features using StandardScaler.
    
    Args:
        train_data (pd.DataFrame): Training data to fit the scaler
        test_data (pd.DataFrame, optional): Test data to transform with the fitted scaler
    
    Returns:
        tuple: (scaled_train_data, scaler, scaled_test_data) - Scaled data and the fitted scaler
    """
    scaler = StandardScaler()
    
    # Fit on training data and transform
    scaled_train = scaler.fit_transform(train_data)
    
    # Also transform test data if provided
    scaled_test = None
    if test_data is not None:
        scaled_test = scaler.transform(test_data)
    
    return scaled_train, scaler, scaled_test

def complete_data_transformation(data):
    """
    Perform complete data transformation including feature engineering and encoding.
    This function is a simplified version of what was in the notebook.
    
    Args:
        data (pd.DataFrame): The housing data
    
    Returns:
        tuple: (features_array, labels_array, feature_names) - 
               Transformed features as numpy array, labels, and feature names
    """
    # Check if we have labels
    has_labels = "median_house_value" in data.columns
    
    if has_labels:
        labels = data["median_house_value"]
        data = data.drop("median_house_value", axis=1)
    else:
        labels = None
    
    # Feature engineering
    engineered_data = create_features(data)
    features = list(engineered_data.columns)
    
    # Split numerical and categorical data
    housing_num = engineered_data.select_dtypes(include=[np.number])
    housing_cat = engineered_data.select_dtypes(exclude=[np.number])
    
    # Impute missing values
    from sklearn.impute import SimpleImputer
    imputer = SimpleImputer(strategy="median")
    imputed = imputer.fit_transform(housing_num)
    
    # Encode categorical data if any exists
    cat_encoded = None
    if not housing_cat.empty:
        from sklearn.preprocessing import OneHotEncoder
        cat_encoder = OneHotEncoder(sparse_output=False)
        cat_encoded = cat_encoder.fit_transform(housing_cat)
        
        # Update features list
        for i, cat_feature in enumerate(housing_cat.columns):
            for category in cat_encoder.categories_[i]:
                features.append(f"{cat_feature}_{category}")
            # Remove the original categorical feature
            features.remove(cat_feature)
    
    # Scale numerical data
    scaler = StandardScaler()
    housing_scaled = scaler.fit_transform(imputed)
    
    # Concatenate all data if we have categorical data
    if cat_encoded is not None:
        output = np.hstack([housing_scaled, cat_encoded])
    else:
        output = housing_scaled
    
    return output, labels, features