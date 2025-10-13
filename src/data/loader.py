"""
Data loading and preprocessing module for the House Price Prediction project.
"""

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder

def load_data(data_path=None):
    """
    Load housing data from CSV file.
    
    Args:
        data_path (str, optional): Path to the CSV file. 
                                  If None, will look for 'housing.csv' in project root.
    
    Returns:
        pd.DataFrame: The loaded housing data
    """
    if data_path is None:
        # Try to find the file in the project root
        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        data_path = os.path.join(current_dir, 'housing.csv')
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Could not find data file at {data_path}")
    
    return pd.read_csv(data_path)

def split_data_simple(data, test_size=0.2, random_state=42):
    """
    Simple random split of data into training and test sets.
    
    Args:
        data (pd.DataFrame): The housing data
        test_size (float): Proportion of data to use for testing
        random_state (int): Random seed for reproducibility
    
    Returns:
        tuple: (X_train, X_test, y_train, y_test) split datasets
    """
    y = data['median_house_value']
    X = data.drop(['median_house_value'], axis=1)
    
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

def split_data_stratified(data, test_size=0.2, random_state=42):
    """
    Stratified split of data based on income category.
    
    Args:
        data (pd.DataFrame): The housing data
        test_size (float): Proportion of data to use for testing
        random_state (int): Random seed for reproducibility
    
    Returns:
        tuple: (train_set, test_set) split datasets
    """
    # Create income category for stratification
    data_with_categories = data.copy()
    data_with_categories['income_cat'] = pd.cut(
        data_with_categories['median_income'],
        bins=[0., 1.5, 3.0, 4.5, 6., np.inf],
        labels=[1, 2, 3, 4, 5]
    )
    
    # Perform stratified split
    split = StratifiedShuffleSplit(n_splits=1, test_size=test_size, random_state=random_state)
    for train_index, test_index in split.split(data_with_categories, data_with_categories['income_cat']):
        train_set = data_with_categories.loc[train_index]
        test_set = data_with_categories.loc[test_index]
    
    # Remove the income_cat column
    for set_ in (train_set, test_set):
        set_.drop('income_cat', axis=1, inplace=True)
    
    return train_set, test_set

def handle_missing_values(data, strategy="median"):
    """
    Handle missing values in the dataset.
    
    Args:
        data (pd.DataFrame): The housing data
        strategy (str): Strategy for imputation ('median', 'mean', etc.)
    
    Returns:
        pd.DataFrame: Data with missing values filled
    """
    imputer = SimpleImputer(strategy=strategy)
    
    # Only apply to numeric columns
    housing_num = data.select_dtypes(include=[np.number])
    
    # Fit and transform
    imputed_array = imputer.fit_transform(housing_num)
    
    # Convert back to DataFrame
    imputed_df = pd.DataFrame(imputed_array, columns=housing_num.columns, index=housing_num.index)
    
    # Replace the numeric columns in the original DataFrame
    result = data.copy()
    result[housing_num.columns] = imputed_df
    
    return result

def encode_categorical_features(data):
    """
    Encode categorical features using one-hot encoding.
    
    Args:
        data (pd.DataFrame): The housing data
    
    Returns:
        tuple: (transformed_data, encoder) - The data with encoded categorical variables 
               and the fitted encoder
    """
    categorical_cols = data.select_dtypes(exclude=[np.number]).columns
    
    if len(categorical_cols) == 0:
        return data, None
    
    # Get categorical columns
    cat_data = data[categorical_cols]
    
    # Apply one-hot encoding
    encoder = OneHotEncoder(sparse_output=False)
    encoded_cats = encoder.fit_transform(cat_data)
    
    # Create new DataFrame with encoded categories
    encoded_cols = []
    for i, col in enumerate(categorical_cols):
        for j, category in enumerate(encoder.categories_[i]):
            encoded_cols.append(f"{col}_{category}")
    
    encoded_df = pd.DataFrame(encoded_cats, columns=encoded_cols, index=data.index)
    
    # Join with numeric data
    numeric_data = data.select_dtypes(include=[np.number])
    result = pd.concat([numeric_data, encoded_df], axis=1)
    
    return result, encoder

def prepare_data_for_training(train_data, test_data=None):
    """
    Prepare data for training by extracting target variable and features.
    
    Args:
        train_data (pd.DataFrame): Training data
        test_data (pd.DataFrame, optional): Test data
    
    Returns:
        tuple: (X_train, y_train, X_test, y_test) - Features and labels for training and testing
    """
    # Extract training features and labels
    y_train = train_data["median_house_value"].copy()
    X_train = train_data.drop("median_house_value", axis=1)
    
    # Extract test features and labels if test data is provided
    if test_data is not None:
        y_test = test_data["median_house_value"].copy()
        X_test = test_data.drop("median_house_value", axis=1)
        return X_train, y_train, X_test, y_test
    
    return X_train, y_train, None, None