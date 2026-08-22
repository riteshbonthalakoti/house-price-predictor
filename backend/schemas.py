from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    size_sqft: float = Field(..., ge=500, le=4000, description="Property size in square feet")
    bedrooms: int = Field(..., ge=1, le=6, description="Number of bedrooms")
    bathrooms: int = Field(..., ge=1, le=4, description="Number of bathrooms")
    age_years: int = Field(..., ge=0, le=40, description="Property age in years")
    location_score: float = Field(..., ge=1, le=10, description="Location score (1-10)")


class PredictResponse(BaseModel):
    predicted_price_lakhs: float = Field(..., description="Predicted price in Lakhs (INR)")
    feature_importance: dict[str, float] = Field(..., description="Relative feature importances")
    model_version: str = Field(default="1.0.0", description="Model version used")
