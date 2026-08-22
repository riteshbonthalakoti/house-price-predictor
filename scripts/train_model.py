import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pickle
import json
import os

def train():
    print("Loading data...")
    df = pd.read_csv('data/house_prices.csv')
    
    features = ['size_sqft', 'bedrooms', 'bathrooms', 'age_years', 'location_score']
    target = 'price_lakhs'
    
    X = df[features]
    y = df[target]
    
    print("Splitting data (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Linear Regression model...")
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    print(f"Metrics:")
    print(f"  MAE:  {mae:.2f} Lakhs")
    print(f"  RMSE: {rmse:.2f} Lakhs")
    print(f"  R2:   {r2:.4f}")
    
    os.makedirs('model', exist_ok=True)
    print("Saving model artifact to model/model.pkl...")
    with open('model/model.pkl', 'wb') as f:
        pickle.dump(model, f)
        
    print("Saving feature names to model/feature_names.json...")
    with open('model/feature_names.json', 'w') as f:
        json.dump(features, f)
        
    print("Done!")

if __name__ == '__main__':
    train()
