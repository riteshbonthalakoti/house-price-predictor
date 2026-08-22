import pandas as pd
import numpy as np
import os

def generate_synthetic_data(num_samples=500, random_seed=42):
    np.random.seed(random_seed)
    
    size_sqft = np.random.uniform(500, 4000, num_samples)
    bedrooms = np.random.randint(1, 7, num_samples)
    bathrooms = np.random.randint(1, 5, num_samples)
    age_years = np.random.randint(0, 41, num_samples)
    location_score = np.random.randint(1, 11, num_samples)
    
    # Linear formula for house price (in Lakhs)
    base_price = 20.0
    true_price = (
        base_price +
        (size_sqft * 0.02) +
        (bedrooms * 3.0) +
        (bathrooms * 2.5) -
        (age_years * 0.8) +
        (location_score * 8.0)
    )
    
    # Add Gaussian noise
    noise = np.random.normal(0, 10, num_samples)
    price_lakhs = true_price + noise
    
    # Ensure no negative prices
    price_lakhs = np.clip(price_lakhs, 10.0, None)
    
    df = pd.DataFrame({
        'size_sqft': size_sqft,
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
        'age_years': age_years,
        'location_score': location_score,
        'price_lakhs': price_lakhs
    })
    
    # Round appropriately
    df['size_sqft'] = df['size_sqft'].round(1)
    df['price_lakhs'] = df['price_lakhs'].round(2)
    
    return df

if __name__ == '__main__':
    os.makedirs('data', exist_ok=True)
    df = generate_synthetic_data()
    df.to_csv('data/house_prices.csv', index=False)
    print(f"Generated {len(df)} synthetic house price records and saved to data/house_prices.csv")
