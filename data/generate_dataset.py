import numpy as np
import pandas as pd
import os

def main():
    # Set seed for reproducibility
    np.random.seed(42)
    
    n_samples = 300
    
    # Generate features
    size_sqft = np.random.uniform(500, 4000, n_samples)
    bedrooms = np.random.randint(1, 7, n_samples)
    bathrooms = np.random.randint(1, 5, n_samples)
    age_years = np.random.randint(0, 41, n_samples)
    location_score = np.random.randint(1, 11, n_samples)
    
    # Linear equation parameters
    # Baseline price: 15 Lakhs
    # positive weights on size_sqft, bedrooms, bathrooms, location_score
    # negative weight on age_years
    base_price = 15.0
    price_lakhs = (
        base_price +
        (size_sqft * 0.05) +
        (bedrooms * 5.0) +
        (bathrooms * 3.0) +
        (location_score * 4.0) -
        (age_years * 0.5)
    )
    
    # Add Gaussian noise
    noise = np.random.normal(0, 12, n_samples)
    price_lakhs = price_lakhs + noise
    
    # Ensure no negative prices (min price of 10 Lakhs)
    price_lakhs = np.clip(price_lakhs, 10.0, None)
    
    # Create DataFrame
    df = pd.DataFrame({
        'size_sqft': np.round(size_sqft, 2),
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
        'age_years': age_years,
        'location_score': location_score,
        'price_lakhs': np.round(price_lakhs, 2)
    })
    
    # Save to data/house_prices.csv
    # Write relative to script folder to guarantee it is saved in the data folder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, 'house_prices.csv')
    df.to_csv(output_path, index=False)
    
    # Output to console
    print(f"Dataset generation complete. Saved to: {output_path}")
    print("\nFirst 5 rows:")
    print(df.head())
    print("\nDescribe statistics:")
    print(df.describe())

if __name__ == '__main__':
    main()
