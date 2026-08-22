"""
House Price Predictor – FastAPI Backend
Loads model from HuggingFace (ritesh1918/house-price-predictor) and serves predictions.
Serves the frontend index.html at / with no extra server required.
"""

import os
import json
import logging
from contextlib import asynccontextmanager
from pathlib import Path

import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from huggingface_hub import hf_hub_download

from schemas import PredictRequest, PredictResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ── Global model state ───────────────────────────────────────────────────────
MODEL_REPO = "ritesh1918/house-price-predictor"
MODEL_FILE = "model.pkl"
FEATURE_NAMES_FILE = "feature_names.json"

model = None
feature_names: list[str] = []
FEATURE_IMPORTANCE: dict[str, float] = {}


def _load_model() -> None:
    """Download model from HuggingFace Hub (cached locally) and load it."""
    global model, feature_names, FEATURE_IMPORTANCE

    # Prefer local copy in model/ directory (avoids repeated downloads)
    local_model = Path(__file__).parent.parent / "model" / MODEL_FILE
    local_features = Path(__file__).parent.parent / "model" / FEATURE_NAMES_FILE

    try:
        if local_model.exists() and local_features.exists():
            logger.info("Loading model from local cache: %s", local_model)
            model_path = str(local_model)
            features_path = str(local_features)
        else:
            logger.info("Downloading model from HuggingFace: %s", MODEL_REPO)
            model_path = hf_hub_download(repo_id=MODEL_REPO, filename=MODEL_FILE)
            features_path = hf_hub_download(repo_id=MODEL_REPO, filename=FEATURE_NAMES_FILE)

        model = joblib.load(model_path)

        with open(features_path) as f:
            feature_names = json.load(f)

        # Build feature importance from linear model coefficients (abs-normalised)
        if hasattr(model, "coef_"):
            coefs = np.abs(model.coef_)
            total = coefs.sum() or 1.0
            FEATURE_IMPORTANCE = {
                name: round(float(coef / total), 4)
                for name, coef in zip(feature_names, coefs)
            }
        else:
            FEATURE_IMPORTANCE = {name: 1.0 / len(feature_names) for name in feature_names}

        logger.info("Model loaded. Features: %s", feature_names)

    except Exception as exc:
        logger.error("Failed to load model: %s", exc)
        raise RuntimeError(f"Model load failed: {exc}") from exc


# ── Lifespan ─────────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    _load_model()
    yield
    # cleanup (none needed)


# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="House Price Predictor API",
    description="ML-powered real estate price prediction service",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Routes ────────────────────────────────────────────────────────────────────
FRONTEND_DIR = Path(__file__).parent.parent / "frontend"
INDEX_HTML = FRONTEND_DIR / "index.html"


@app.get("/", response_class=HTMLResponse)
def serve_ui():
    """Serve the dashboard UI."""
    if INDEX_HTML.exists():
        return HTMLResponse(content=INDEX_HTML.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>Frontend not found</h1><p>Place index.html in house-price-predictor/frontend/</p>", status_code=404)


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest) -> PredictResponse:
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded yet")

    # Build feature vector in the correct order
    feature_map = {
        "size_sqft": req.size_sqft,
        "bedrooms": req.bedrooms,
        "bathrooms": req.bathrooms,
        "age_years": req.age_years,
        "location_score": req.location_score,
    }
    X = np.array([[feature_map[f] for f in feature_names]])

    prediction = float(model.predict(X)[0])
    prediction = max(0.0, round(prediction, 2))

    return PredictResponse(
        predicted_price_lakhs=prediction,
        feature_importance=FEATURE_IMPORTANCE,
        model_version="1.0.0",
    )
