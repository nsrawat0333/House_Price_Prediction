"""
Main script for the House Price Prediction project.
This script orchestrates the end-to-end machine learning workflow.
"""

import os
import argparse
import time

# Import modules from our package
from src.data.loader import load_data, split_data_stratified
from src.features.engineering import complete_data_transformation
from src.models.train_evaluate import (train_linear_regression, 
                                      train_decision_tree,
                                      train_random_forest, 
                                      evaluate_model, 
                                      cross_validate_model,
                                      tune_random_forest,
                                      save_model,
                                      feature_importance)
from src.visualization.visualize import (plot_histogram,
                                        plot_scatter_map,
                                        plot_correlation_matrix,
                                        plot_predictions_vs_actual,
                                        plot_feature_importance)
from src.utils.helpers import check_dependencies, create_output_directory

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='House Price Prediction')
    parser.add_argument('--data_path', type=str, default=None,
                        help='Path to the housing dataset CSV file')
    parser.add_argument('--test_size', type=float, default=0.2,
                        help='Proportion of data to use for testing')
    parser.add_argument('--random_state', type=int, default=42,
                        help='Random seed for reproducibility')
    parser.add_argument('--visualize', action='store_true',
                        help='Enable data visualization')
    parser.add_argument('--tune', action='store_true',
                        help='Tune model hyperparameters')
    parser.add_argument('--model_type', type=str, default='rf',
                        choices=['linear', 'dt', 'rf', 'all'],
                        help='Model type to train (linear, dt=decision tree, rf=random forest, all)')
    parser.add_argument('--save_model', action='store_true',
                        help='Save the best model')
    
    return parser.parse_args()

def main():
    """Main function to run the pipeline."""
    # Check if required packages are installed
    if not check_dependencies():
        return
    
    # Parse command line arguments
    args = parse_arguments()
    
    # Create output directory
    output_dir = create_output_directory()
    
    # Record start time
    start_time = time.time()
    
    print("=== House Price Prediction Project ===")
    print("\n1. Loading data...")
    data = load_data(args.data_path)
    print(f"Data loaded: {data.shape[0]} rows, {data.shape[1]} columns")
    
    if args.visualize:
        print("\n2. Visualizing data...")
        # Plot histograms
        plot_histogram(data)
        
        # Plot geographic scatter plot
        plot_scatter_map(data)
        
        # Plot correlation matrix
        plot_correlation_matrix(data)
    
    print("\n3. Splitting data...")
    train_set, test_set = split_data_stratified(data, test_size=args.test_size, 
                                               random_state=args.random_state)
    print(f"Train set: {train_set.shape[0]} rows")
    print(f"Test set: {test_set.shape[0]} rows")
    
    print("\n4. Transforming data...")
    # Transform training data
    train_data, train_labels, features = complete_data_transformation(train_set)
    # Transform test data
    test_data, test_labels, _ = complete_data_transformation(test_set)
    
    print(f"Transformed training data: {train_data.shape}")
    print(f"Transformed test data: {test_data.shape}")
    
    print("\n5. Training and evaluating models...")
    models = {}
    evaluation_results = {}
    
    # Train models based on user selection
    if args.model_type in ['linear', 'all']:
        print("\n--- Linear Regression ---")
        models['linear'] = train_linear_regression(train_data, train_labels)
        evaluation_results['linear'] = evaluate_model(models['linear'], test_data, test_labels, "Linear Regression")
        cross_validate_model(models['linear'], train_data, train_labels, model_name="Linear Regression")
        
        if args.visualize:
            plot_predictions_vs_actual(test_labels, evaluation_results['linear']['predictions'], 
                                      "Linear Regression: Actual vs Predicted")
    
    if args.model_type in ['dt', 'all']:
        print("\n--- Decision Tree ---")
        models['dt'] = train_decision_tree(train_data, train_labels, random_state=args.random_state)
        evaluation_results['dt'] = evaluate_model(models['dt'], test_data, test_labels, "Decision Tree")
        cross_validate_model(models['dt'], train_data, train_labels, model_name="Decision Tree")
        
        if args.visualize:
            plot_predictions_vs_actual(test_labels, evaluation_results['dt']['predictions'], 
                                      "Decision Tree: Actual vs Predicted")
            plot_feature_importance(feature_importance(models['dt'], features))
    
    if args.model_type in ['rf', 'all']:
        print("\n--- Random Forest ---")
        if args.tune:
            print("Tuning Random Forest hyperparameters...")
            models['rf'], best_params, _ = tune_random_forest(train_data, train_labels, random_state=args.random_state)
        else:
            models['rf'] = train_random_forest(train_data, train_labels, random_state=args.random_state)
        
        evaluation_results['rf'] = evaluate_model(models['rf'], test_data, test_labels, "Random Forest")
        cross_validate_model(models['rf'], train_data, train_labels, model_name="Random Forest")
        
        if args.visualize:
            plot_predictions_vs_actual(test_labels, evaluation_results['rf']['predictions'], 
                                      "Random Forest: Actual vs Predicted")
            plot_feature_importance(feature_importance(models['rf'], features))
    
    # Find the best model based on test RMSE
    if models:
        best_model_name = min(evaluation_results, key=lambda k: evaluation_results[k]['rmse'])
        best_model = models[best_model_name]
        print(f"\nBest model: {best_model_name}")
        print(f"Test RMSE: {evaluation_results[best_model_name]['rmse']:.2f}")
        
        if args.save_model:
            model_path = os.path.join(output_dir, f"{best_model_name}_model.pkl")
            save_model(best_model, model_path)
    
    # Print execution time
    end_time = time.time()
    print(f"\nExecution completed in {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()