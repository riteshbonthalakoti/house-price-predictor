---
title: House Price Predictor API
emoji: 🏠
colorFrom: indigo
colorTo: purple
sdk: docker
pinned: false
license: mit
short_description: FastAPI backend for ML house price prediction
---

# House Price Predictor — FastAPI Backend

This Space serves the FastAPI backend for the ProphecyAI house price prediction app.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Health check |
| `GET` | `/health` | Model status |
| `POST` | `/predict` | Predict price |

## Example Request

```bash
curl -X POST https://ritesh1918-house-price-predictor.hf.space/predict \
  -H "Content-Type: application/json" \
  -d '{"size_sqft": 1850, "bedrooms": 3, "bathrooms": 2.5, "age_years": 8, "location_score": 8.2}'
```

## Frontend

The UI is deployed at: **https://house-price-predictor.pages.dev**
