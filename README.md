# House_Price_Prediction

A machine learning project to predict house prices using the California housing dataset, with a beautiful interactive web interface and bilingual (English/Hindi) support.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Dataset](#dataset)
- [System Requirements](#system-requirements)
- [Libraries Used](#libraries-used)
- [Project Features](#project-features)
- [Project Structure](#project-structure)
- [How to Run](#how-to-run)
- [Web Interface](#web-interface)
- [Results](#results)
- [Future Scope](#future-scope)
- [References](#references)

---

## Project Overview

This project aims to predict house prices in California using various features such as location, median income, and housing characteristics. The solution uses machine learning algorithms (Linear Regression, Decision Tree, Random Forest) and includes data preprocessing, feature engineering, model training, and evaluation.

The project features a complete modular Python architecture with separate components for data loading, feature engineering, model training, and visualization. It also includes an interactive web application with a beautiful UI built using Flask, Bootstrap, and modern front-end techniques with bilingual support (English and Hindi).

---

## Dataset

- **Source:** [California Housing Prices Dataset (Kaggle)](https://www.kaggle.com/datasets/camnugent/california-housing-prices)
- **Features:** longitude, latitude, housing_median_age, total_rooms, total_bedrooms, population, households, median_income, ocean_proximity, median_house_value

---

## System Requirements

- Windows/Linux/Mac OS
- Python 3.7+
- Jupyter Notebook or any Python IDE
- Minimum 4GB RAM

---

## Libraries Used

- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn
- joblib
- Flask (for web application)
- Bootstrap 5 (for responsive UI)
- JavaScript (for interactive features)

## Project Features

- **Modular Code Structure**: Well-organized Python modules with proper separation of concerns
- **Multiple ML Models**: Linear Regression, Decision Tree, and Random Forest implementations
- **Interactive Web Interface**: Beautiful UI with Bootstrap 5 and custom CSS
- **Bilingual Support**: Full Hindi/English interface with language switching functionality
- **Data Visualization**: Interactive charts showing model performance and feature importance
- **Form Validation**: Client-side validation for all input fields
- **Responsive Design**: Works well on desktop and mobile devices
- **Interactive Elements**: Tooltips, animations, and visual feedback throughout the application
- **Error Handling**: Comprehensive error handling on both client and server sides

---

## Project Structure

```
House_Price_Prediction/
│
├── main.py                        # Main script to run the pipeline
├── housing.csv                    # Dataset file
├── Project_template_MS AI(housepriceprediction).pdf  # Project report/presentation
├── House_Price_Prediction.ipynb   # Original Jupyter notebook
│
├── src/                           # Source code
│   ├── data/                      # Data loading and preprocessing
│   │   └── loader.py              # Functions for loading and preprocessing data
│   │
│   ├── features/                  # Feature engineering
│   │   └── engineering.py         # Functions for feature engineering
│   │
│   ├── models/                    # Model training and evaluation
│   │   └── train_evaluate.py      # Functions for model training and evaluation
│   │
│   ├── visualization/             # Data visualization
│   │   └── visualize.py           # Functions for data visualization
│   │
│   └── utils/                     # Utility functions
│       └── helpers.py             # Helper functions
│
├── webapp/                        # Web application
│   ├── app.py                     # Flask application
│   ├── templates/                 # HTML templates
│   │   ├── base.html              # Base template
│   │   └── index.html             # Main page template
│   │
│   └── static/                    # Static files
│       ├── css/                   # CSS styles
│       ├── js/                    # JavaScript
│       └── img/                   # Images
│
├── output/                        # Generated output (models, results)
├── README.md                      # Project documentation
└── .gitignore
```

---

## How to Run

1. Clone the repository:
```bash
git clone https://github.com/nsrawat0333/House_Price_Prediction.git
cd House_Price_Prediction
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. To train the model from command line:
```bash
python main.py --model_type rf --save_model
```
   Options for model_type: 'lr' (Linear Regression), 'dt' (Decision Tree), 'rf' (Random Forest)

4. To run the web application:
```bash
python -m webapp.app
```
   Then open your browser and navigate to http://127.0.0.1:5000

5. For convenience, Windows users can run the web application using the batch file:
```bash
run_webapp.bat
```

## Web Interface

The web interface includes the following features:

1. **Interactive Dashboard**: Visualizes model performance and feature importance
2. **Prediction Form**: Enter house details to get a price prediction
3. **Bilingual Support**: Toggle between English and Hindi throughout the interface
4. **Visual Feedback**: Animations for predictions and user interactions
5. **Responsive Design**: Works on both desktop and mobile devices

1. **Clone the repository:**
    ```sh
    git clone https://github.com/nsrawat0333/House_Price_Prediction.git
    cd House_Price_Prediction
    ```

2. **Install required libraries:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Run the pipeline:**
    ```sh
    python main.py
    ```

4. **Optional arguments:**
    ```
    --data_path PATH     Path to the housing dataset CSV file
    --test_size FLOAT    Proportion of data to use for testing (default: 0.2)
    --random_state INT   Random seed for reproducibility (default: 42)
    --visualize          Enable data visualization
    --tune               Tune model hyperparameters
    --model_type TYPE    Model type to train: linear, dt, rf, all (default: rf)
    --save_model         Save the best model
    ```

### Example Commands

Train all models and show visualizations:
```sh
python main.py --visualize --model_type all
```

Train and tune a Random Forest model:
```sh
python main.py --tune --model_type rf --save_model
```

### Using the Web Application

The project includes a web interface to interact with the trained model:

1. **Train and save a model first:**
   ```sh
   python main.py --model_type rf --save_model
   ```

2. **Run the Flask web application:**
   ```sh
   cd webapp
   python app.py
   ```

3. **Open your browser** and navigate to: http://127.0.0.1:5000

The web interface provides:
- Interactive input form for making predictions
- Visualizations of model performance
- Feature importance analysis
- Sample data from the dataset

### Alternative: Using Jupyter Notebook
- Launch Jupyter Notebook and open `House_Price_Prediction.ipynb`
- Run all cells to see the original workflow and results

---

## Results

- The Random Forest model achieved the best performance with the lowest RMSE and MAE.
- Actual vs Predicted house prices show a strong correlation.
- Feature importance analysis highlights median income and location as key predictors.

*(For detailed results and visualizations, see the notebook.)*

---

## Future Scope

- Integrate more advanced models like XGBoost or deep learning.
- Add more features (e.g., crime rate, school quality).
- Enhance the web application with additional visualizations and interactive features.
- Deploy the web application to a cloud platform for wider access.
- Automate data updates and model retraining.

---

## References

- [California Housing Prices Dataset (Kaggle)](https://www.kaggle.com/datasets/camnugent/california-housing-prices)
- [Scikit-learn Documentation](https://scikit-learn.org/stable/)
- [Python Official Documentation](https://docs.python.org/3/)
- Aurélien Géron, *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow*
- [GitHub Repository](https://github.com/nsrawat0333/House_Price_Prediction)

---
