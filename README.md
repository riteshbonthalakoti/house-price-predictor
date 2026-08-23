# 🏠 ProphecyAI — House Price Predictor

A full-stack ML demo built as a **live teaching session** showcasing end-to-end machine learning: a Linear Regression model trained on synthetic housing data, and deployed as a 100% serverless, 0ms-latency web dashboard hosted on Cloudflare Pages — all wired together and accessible from any device.

---

## 🌐 Live Demo

| | Link |
|---|---|
| **Frontend Dashboard** | **[house-price-predictor.pages.dev](https://house-price-predictor.pages.dev)** |
| **Model on Hugging Face** | [huggingface.co/ritesh1918/house-price-predictor](https://huggingface.co/ritesh1918/house-price-predictor) |

> ⚡ **Serverless AI**: This application does not use a backend API. The machine learning model inference is embedded directly into the frontend JavaScript, resulting in **zero millisecond latency**, zero cold-starts, and 100% free hosting.

---

## 🏗️ Architecture

```
Synthetic Data (300 rows)
        │
        ▼
┌──────────────────┐
│  Google Colab    │  ← model/train.ipynb (teaching notebook)
│  Training        │    Linear Regression, sklearn
│  Notebook        │    Extracts intercept & weights
└────────┬─────────┘
         │ 
         ▼
┌──────────────────┐
│  HTML Dashboard  │  ← frontend/index.html
│  Cloudflare Pages│    Client-Side JS calculates Price
│                  │    Price = b + (size*w1) + (beds*w2) ...
└──────────────────┘
```

---

## 🧰 Tech Stack

| Layer | Technology |
|-------|-----------|
| Model training | Python, scikit-learn (LinearRegression), NumPy, pandas |
| Training environment | Google Colab (`model/train.ipynb`) |
| Web Application | Vanilla HTML/CSS/JS — zero frameworks |
| Web Hosting | Cloudflare Pages (Free Tier) |
| Architecture | 100% Serverless / Client-Side Inference |

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

The web app is a single static HTML file — no servers to start, no dependencies to install. Open it directly in any browser:

```bash
# Option A: open directly
open frontend/index.html

# Option B: serve locally
cd frontend
python -m http.server 4321
```

---

## 📁 Project Structure

```
house-price-predictor/
├── data/
│   └── generate_dataset.py     # Synthetic data generator
├── frontend/
│   └── index.html              # Single-file dashboard (no build step)
├── model/
│   ├── train.ipynb             # Teaching notebook (Colab-ready)
│   ├── train_study_guide.pdf   # Study guide generated from notebook
│   └── feature_names.json      # Feature metadata
├── scripts/
│   ├── create_google_form.py   # Feedback form generation script
│   └── generate_study_guide.py # PDF generation script
├── intro-slides.html           # Presentation slide deck
├── resources.html              # Session links hub
└── README.md                   # This file
```

---

## 🤝 About

Built as a **live teaching demo** for a session on Machine Learning fundamentals — specifically to explain Linear Regression by building something real and deployed, not just a notebook exercise.
