---
language:
- en
license: mit
tags:
- regression
- scikit-learn
- tabular
datasets:
- synthetic
metrics:
- mae
- rmse
- r2
model-index:
- name: Linear Regression House Price Predictor
  results:
  - task:
      type: tabular-regression
      name: Tabular Regression
    dataset:
      type: synthetic
      name: Synthetic Housing Prices
    metrics:
    - type: mae
      value: 8.78
      name: Mean Absolute Error
      unit: Lakhs
    - type: rmse
      value: 11.23
      name: Root Mean Squared Error
      unit: Lakhs
    - type: r2
      value: 0.9566
      name: R2 Score
---

# Linear Regression House Price Predictor

A simple `LinearRegression` model trained on a synthetic housing dataset. Built as a teaching artifact to demonstrate an end-to-end Machine Learning engineering workflow (data generation -> model training -> API serving -> frontend UI).

## Model Details
- **Algorithm**: Ordinary Least Squares (OLS) Linear Regression (`scikit-learn`)
- **Features used**:
  - `size_sqft`: Size of the property in square feet (float)
  - `bedrooms`: Number of bedrooms (int)
  - `bathrooms`: Number of bathrooms (int)
  - `age_years`: Age of the property in years (int)
  - `location_score`: Neighborhood desirability score from 1-10 (int)
- **Target**: `price_lakhs`: Price of the property in Lakhs (float)

## Training Data & Parameters
The training dataset is synthetically generated (300 samples) with features linearly combined plus Gaussian noise (mean=0, std=12) to simulate realistic market variability.
- **Train/Test Split**: 80/20
- **Random State**: 42

## Performance Metrics
- **Mean Absolute Error (MAE)**: 8.78 Lakhs
- **Root Mean Squared Error (RMSE)**: 11.23 Lakhs
- **R² Score**: 0.9566

## How to Use
```python
import pickle
import numpy as np

# Load model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# Input format: [size_sqft, bedrooms, bathrooms, age_years, location_score]
sample_input = np.array([[1500, 3, 2, 5, 8]])
prediction = model.predict(sample_input)[0]
print(f"Predicted Price: {prediction:.2f} Lakhs")
```
