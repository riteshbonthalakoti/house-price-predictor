from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import pickle
import json
import numpy as np
import os

app = FastAPI(title="House Price Predictor API")

# Allow all origins for the demo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model and features on startup
# We look for them in the parent directory's 'model' folder when running from root
MODEL_PATH = "model/model.pkl"
FEATURES_PATH = "model/feature_names.json"

model = None
feature_names = []

@app.on_event("startup")
def load_artifacts():
    global model, feature_names
    try:
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
        with open(FEATURES_PATH, "r") as f:
            feature_names = json.load(f)
        print("Model and features loaded successfully.")
    except Exception as e:
        print(f"Error loading artifacts: {e}")

class PredictionRequest(BaseModel):
    size_sqft: float = Field(..., ge=500, le=4000, description="Size of the house in sqft")
    bedrooms: int = Field(..., ge=1, le=6, description="Number of bedrooms")
    bathrooms: int = Field(..., ge=1, le=4, description="Number of bathrooms")
    age_years: int = Field(..., ge=0, le=40, description="Age of the house in years")
    location_score: int = Field(..., ge=1, le=10, description="Location desirability score (1-10)")

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "features_loaded": len(feature_names) > 0
    }

@app.get("/model-info")
def model_info():
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    # We log these at training, ideally we'd load them from a metrics.json,
    # but for simplicity we'll re-calculate or just return coefficients
    coefficients = dict(zip(feature_names, model.coef_))
    
    return {
        "model_type": "LinearRegression",
        "intercept": model.intercept_,
        "coefficients": coefficients,
        "note": "Linear Regression formula: price = intercept + sum(coef_i * feature_i)"
    }

@app.post("/predict")
def predict(request: PredictionRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    # Create input array in the exact order of training features
    input_data = np.array([[
        request.size_sqft,
        request.bedrooms,
        request.bathrooms,
        request.age_years,
        request.location_score
    ]])
    
    prediction = model.predict(input_data)[0]
    
    # Ensure prediction isn't negative
    prediction = max(10.0, float(prediction))
    
    return {
        "predicted_price_lakhs": round(prediction, 2),
        "model_confidence_note": "Based on a synthetic linear dataset with R2 ~ 0.90",
        "inputs": request.dict()
    }
