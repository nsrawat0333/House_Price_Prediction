"""
Utility functions for the House Price Prediction project.
"""

import os
import numpy as np

def get_project_root():
    """
    Get the absolute path to the project root directory.
    
    Returns:
        str: Absolute path to the project root
    """
    # Navigate up from the current file's directory to the project root
    # (src/utils/ -> src/ -> project_root/)
    current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return current_dir

def display_scores(scores):
    """
    Display cross-validation scores with mean and standard deviation.
    
    Args:
        scores (np.ndarray): Array of scores
    """
    print("Scores:", scores)
    print("Mean:", scores.mean())
    print("Standard deviation:", scores.std())
    return {
        "scores": scores,
        "mean": scores.mean(),
        "std": scores.std()
    }

def check_dependencies():
    """
    Check if all required dependencies are installed.
    
    Returns:
        bool: True if all dependencies are available, False otherwise
    """
    required_packages = [
        'pandas',
        'numpy',
        'matplotlib',
        'seaborn',
        'scikit-learn',
        'joblib'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("Missing dependencies:", missing_packages)
        print("Please install them with:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    print("All dependencies are installed.")
    return True

def create_output_directory():
    """
    Create output directory for saving models and results if it doesn't exist.
    
    Returns:
        str: Path to the output directory
    """
    output_dir = os.path.join(get_project_root(), "output")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir