"""
Flask web application for House Price Prediction.
"""

import os
import sys
import numpy as np
import pandas as pd
import joblib
from flask import Flask, render_template, request, jsonify
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Import project modules
from src.data.loader import load_data
from src.features.engineering import create_features, complete_data_transformation
from src.models.train_evaluate import train_random_forest, evaluate_model, feature_importance
from src.visualization.visualize import plot_predictions_vs_actual

# Initialize Flask app
app = Flask(__name__)

# Global variables
MODEL_PATH = os.path.join(project_root, 'output', 'rf_model.pkl')
DATA_PATH = os.path.join(project_root, 'housing.csv')


def train_and_save_model_if_needed():
    """Train and save the model if it doesn't exist."""
    os.makedirs(os.path.join(project_root, 'output'), exist_ok=True)
    
    if not os.path.exists(MODEL_PATH):
        print("Training new model...")
        # Load and preprocess data
        data = load_data(DATA_PATH)
        # Split into train/test
        train_size = int(0.8 * len(data))
        train_data = data.iloc[:train_size]
        test_data = data.iloc[train_size:]
        
        # Transform data
        X_train, y_train, features = complete_data_transformation(train_data)
        
        # Train model
        model = train_random_forest(X_train, y_train)
        
        # Save model, features, and transformation info
        joblib.dump(model, MODEL_PATH)
        joblib.dump(features, os.path.join(project_root, 'output', 'features.pkl'))
        
        # Also save the unique categories for ocean_proximity to ensure consistent encoding
        ocean_prox_values = data['ocean_proximity'].unique().tolist()
        joblib.dump(ocean_prox_values, os.path.join(project_root, 'output', 'ocean_proximity_categories.pkl'))
        
        print("Model trained and saved.")
    else:
        print("Model already exists.")


def load_trained_model():
    """Load the trained model and features."""
    model = joblib.load(MODEL_PATH)
    features = joblib.load(os.path.join(project_root, 'output', 'features.pkl'))
    return model, features


def fig_to_base64(fig):
    """Convert matplotlib figure to base64 string for HTML display."""
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    return img_str


def generate_feature_importance_plot(model, features):
    """Generate feature importance plot."""
    importances = feature_importance(model, features)
    top_features = importances.head(10)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_features.values, y=top_features.index)
    plt.title('Top 10 Feature Importances')
    plt.tight_layout()
    
    img_str = fig_to_base64(plt.gcf())
    plt.close()
    return img_str


def generate_prediction_scatter_plot(actual, predicted):
    """Generate scatter plot of actual vs predicted values."""
    plt.figure(figsize=(8, 8))
    plt.scatter(actual, predicted, alpha=0.5)
    plt.xlabel('Actual House Prices')
    plt.ylabel('Predicted House Prices')
    plt.title('Actual vs Predicted House Prices')
    
    # Add diagonal line
    min_val = min(actual.min(), predicted.min())
    max_val = max(actual.max(), predicted.max())
    plt.plot([min_val, max_val], [min_val, max_val], 'r--')
    
    plt.tight_layout()
    img_str = fig_to_base64(plt.gcf())
    plt.close()
    return img_str


def prepare_sample_data():
    """Prepare some sample data from the dataset."""
    data = load_data(DATA_PATH)
    return data.head(5).to_dict(orient='records')

def get_ocean_proximity_categories():
    """Get the ocean proximity categories used during training."""
    categories_path = os.path.join(project_root, 'output', 'ocean_proximity_categories.pkl')
    if os.path.exists(categories_path):
        return joblib.load(categories_path)
    else:
        # If not saved yet, use the ones from the original dataset
        data = load_data(DATA_PATH)
        return data['ocean_proximity'].unique().tolist()


@app.route('/')
def home():
    """Home page view."""
    # Ensure model is trained
    train_and_save_model_if_needed()
    
    # Load model and features
    model, saved_features = load_trained_model()
    
    # Generate feature importance plot
    feature_plot = generate_feature_importance_plot(model, saved_features)
    
    # Get sample data
    sample_data = prepare_sample_data()
    
    # Load data for visualization
    data = load_data(DATA_PATH)
    test_size = int(0.2 * len(data))
    test_data = data.iloc[:test_size]
    
    # Transform test data
    X_test, y_test, _ = complete_data_transformation(test_data)
    
    # Handle feature dimensionality mismatch if needed
    if X_test.shape[1] != len(saved_features):
        print(f"Feature mismatch: Input has {X_test.shape[1]} features, model expects {len(saved_features)}")
        # This is a simplified approach - in production you'd need more sophisticated handling
        if X_test.shape[1] < len(saved_features):
            # Pad with zeros if missing features
            pad_width = ((0, 0), (0, len(saved_features) - X_test.shape[1]))
            X_test = np.pad(X_test, pad_width=pad_width, mode='constant', constant_values=0)
        else:
            # Trim if too many features
            X_test = X_test[:, :len(saved_features)]
    
    # Make predictions on test data
    predictions = model.predict(X_test)
    
    # Generate predictions plot
    predictions_plot = generate_prediction_scatter_plot(y_test, predictions)
    
    # Get statistics
    from sklearn.metrics import mean_squared_error, r2_score
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)
    
    # Get feature ranges for the form
    feature_ranges = {}
    numeric_columns = data.select_dtypes(include=[np.number]).columns
    for col in numeric_columns:
        if col != 'median_house_value':
            feature_ranges[col] = {
                'min': data[col].min(),
                'max': data[col].max(),
                'mean': data[col].mean(),
                'default': data[col].median()
            }
    
    # Get ocean proximity categories - use saved categories to ensure consistency
    ocean_proximity_values = get_ocean_proximity_categories()
    
    return render_template(
        'index.html',
        feature_plot=feature_plot,
        predictions_plot=predictions_plot,
        sample_data=sample_data,
        rmse=rmse,
        r2=r2,
        feature_ranges=feature_ranges,
        ocean_proximity_values=ocean_proximity_values
    )


@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction requests."""
    # Get form data
    try:
        # Extract features from form
        features_dict = {}
        for field in request.form:
            if field != 'csrf_token':
                features_dict[field] = float(request.form[field]) if field != 'ocean_proximity' else request.form[field]
        
        # Create DataFrame with the input
        input_df = pd.DataFrame([features_dict])
        
        # Load model and features
        model, saved_features = load_trained_model()
        
        # Make a copy of the original dataset to match structure
        data = load_data(DATA_PATH)
        dummy_row = data.iloc[0:1].copy()
        
        # Replace values with the input values
        for col in features_dict:
            if col in dummy_row.columns:
                dummy_row[col] = features_dict[col]
        
        # Transform input using the same pipeline
        X_input, _, _ = complete_data_transformation(dummy_row)
        
        # Handle feature dimensionality mismatch if needed
        if X_input.shape[1] != len(saved_features):
            print(f"Feature mismatch: Input has {X_input.shape[1]} features, model expects {len(saved_features)}")
            # This is a simplified approach - in production you'd need more sophisticated handling
            if X_input.shape[1] < len(saved_features):
                # Pad with zeros if missing features
                pad_width = ((0, 0), (0, len(saved_features) - X_input.shape[1]))
                X_input = np.pad(X_input, pad_width=pad_width, mode='constant', constant_values=0)
            else:
                # Trim if too many features
                X_input = X_input[:, :len(saved_features)]
        
        # Make prediction
        prediction = model.predict(X_input)[0]
        
        # Return result
        return jsonify({
            'success': True,
            'prediction': float(prediction),
            'formatted_prediction': f"${prediction:,.2f}"
        })
    
    except Exception as e:
        import traceback
        traceback_str = traceback.format_exc()
        print(traceback_str)
        return jsonify({
            'success': False,
            'error': str(e)
        })


if __name__ == '__main__':
    app.run(debug=True, port=5000)