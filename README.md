# 🏠 ProphecyAI — House Price Predictor

A full-stack ML demo built as a **live teaching session** showcasing end-to-end machine learning: a Linear Regression model trained on synthetic housing data, served via a FastAPI backend, with a light-mode glassmorphism dashboard deployed on Cloudflare Pages — all wired together and accessible from any device.

---

## 🌐 Live Demo

| | Link |
|---|---|
| **Frontend Dashboard** | **[house-price-predictor.pages.dev](https://house-price-predictor.pages.dev)** |
| **API Health Check** | [house-price-predictor-api-lq99.onrender.com/health](https://house-price-predictor-api-lq99.onrender.com/health) |
| **API Docs (Swagger)** | [house-price-predictor-api-lq99.onrender.com/docs](https://house-price-predictor-api-lq99.onrender.com/docs) |
| **Model on Hugging Face** | [huggingface.co/ritesh1918/house-price-predictor](https://huggingface.co/ritesh1918/house-price-predictor) |

> ⚠️ The backend runs on Render's free tier — first request after inactivity may take ~20 seconds to wake up. The UI shows a graceful loading state while this happens.

---

## 🏗️ Architecture

```
Synthetic Data (300 rows)
        │
        ▼
┌──────────────────┐
│  Google Colab    │  ← model/train.ipynb (teaching notebook)
│  Training        │    Linear Regression, sklearn
│  Notebook        │    MAE: 8.78L  RMSE: 11.23L  R²: 0.9566
└────────┬─────────┘
         │ joblib.dump(model)
         ▼
┌──────────────────┐
│  Hugging Face    │  ← ritesh1918/house-price-predictor
│  Model Hub       │    model.pkl + feature_names.json
└────────┬─────────┘
         │ hf_hub_download() on startup
         ▼
┌──────────────────┐
│  FastAPI Backend │  ← backend/main.py
│  on Render.com   │    POST /predict → price + feature importance
└────────┬─────────┘
         │ fetch('/predict')
         ▼
┌──────────────────┐
│  HTML Dashboard  │  ← frontend/index.html
│  Cloudflare Pages│    Sliders → Predict → Animated price + bar chart
└──────────────────┘
```

---

## 🧰 Tech Stack

| Layer | Technology |
|-------|-----------|
| Model training | Python, scikit-learn (LinearRegression), NumPy, pandas |
| Training environment | Google Colab (`model/train.ipynb`) |
| Model hosting | Hugging Face Hub |
| Backend API | FastAPI, uvicorn, joblib, pydantic |
| Backend hosting | Render.com (free tier) |
| Frontend | Vanilla HTML/CSS/JS — zero frameworks |
| Frontend hosting | Cloudflare Pages |
| CI/CD | GitHub Actions (keep-warm ping every 10 min) |
| IDE | [Antigravity IDE](https://antigravity.dev) |

---

## 📓 Teaching Notebook

The notebook at [`model/train.ipynb`](model/train.ipynb) is designed for a live classroom session. It walks through:

1. What is Machine Learning? (traditional code vs ML)
2. The Linear Regression equation — `ŷ = w₁x₁ + w₂x₂ + ... + b`
3. Generating the synthetic housing dataset
4. Exploratory data analysis with matplotlib/seaborn
5. Training with `model.fit(X_train, y_train)`
6. **True vs Learned coefficients** comparison chart
7. Evaluation: MAE, RMSE, R² + Actual vs Predicted scatter
8. Predicting on new houses
9. Pushing to Hugging Face Hub

**Open in Colab:**
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/riteshbonthalakoti/house-price-predictor/blob/master/model/train.ipynb)

---

## 📊 Model Performance

Trained on 240 samples (80/20 split), tested on 60 unseen samples:

| Metric | Value | Meaning |
|--------|-------|---------|
| **R²** | **0.9566** | 95.7% of price variance explained |
| **MAE** | **8.78 Lakhs** | Average prediction error |
| **RMSE** | **11.23 Lakhs** | Error penalising large outliers |

The model correctly rediscovers the approximate ground-truth coefficients used to generate the data — a key teaching moment in the notebook.

---

## 🚀 Running Locally

### Backend

```bash
cd house-price-predictor/backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The model will download automatically from Hugging Face on first startup.

Test it:
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"size_sqft": 1850, "bedrooms": 3, "bathrooms": 2.5, "age_years": 8, "location_score": 8.2}'
```

Expected response:
```json
{
  "predicted_price_lakhs": 160.54,
  "feature_importance": {
    "size_sqft": 0.0039,
    "bedrooms": 0.4679,
    "bathrooms": 0.1746,
    "age_years": 0.0411,
    "location_score": 0.3125
  },
  "model_version": "1.0.0"
}
```

### Frontend

The frontend is a single static HTML file — open it directly in any browser:

```bash
# Option A: open directly
open house-price-predictor/frontend/index.html

# Option B: serve locally (if testing API calls)
cd house-price-predictor/frontend
python -m http.server 4321
```

By default the frontend points to the live Render backend. To use your local backend instead, change line 1 of the `<script>` block in `index.html`:

```js
const API = 'http://localhost:8000';  // local
```

---

## 📁 Project Structure

```
house-price-predictor/
├── .github/
│   └── workflows/
│       └── keep-warm.yml       # Pings Render /health every 10 min
├── backend/
│   ├── main.py                 # FastAPI app
│   ├── schemas.py              # Pydantic request/response models
│   ├── requirements.txt
│   ├── Dockerfile              # For containerised deployments
│   └── README.md               # Hugging Face Space config
├── data/
│   └── generate_dataset.py     # Synthetic data generator
├── frontend/
│   └── index.html              # Single-file dashboard (no build step)
├── model/
│   ├── train.ipynb             # Teaching notebook (Colab-ready)
│   ├── model.pkl               # Trained LinearRegression model
│   ├── feature_names.json      # Feature order for inference
│   └── README.md               # Hugging Face model card
├── tests/
│   └── test_predict.py         # API smoke tests
├── render.yaml                 # Render deployment config
└── README.md
```

---

## 🤝 About

Built as a **live teaching demo** for a session on Machine Learning fundamentals — specifically to explain Linear Regression by building something real and deployed, not just a notebook exercise.

Built with ❤️ using [Antigravity IDE](https://antigravity.dev) by Google DeepMind.
