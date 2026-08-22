# House Price Predictor (Live Demo)

A full-stack ML application for predicting house prices using a synthetic dataset and a Linear Regression model. 
Built as a teaching artifact to demonstrate an end-to-end Machine Learning engineering lifecycle.

## Architecture

- **Data Generation**: `scripts/generate_data.py` creates a synthetic housing dataset (`data/house_prices.csv`).
- **Model Training**: `scripts/train_model.py` trains a Scikit-Learn `LinearRegression` model.
- **Backend**: FastAPI app serving predictions (`backend/main.py`), deployed to Hugging Face Spaces.
- **Frontend**: A rich, interactive dashboard built with vanilla HTML/CSS/JS (Stitch aesthetics), deployed to Cloudflare Pages.

## Live Links
- **Frontend App**: *See Cloudflare Pages Deployment URL*
- **API Endpoint**: `https://ritesh1918-house-price-api.hf.space`
- **Model Space**: `https://huggingface.co/spaces/ritesh1918/house-price-api`

## Running Locally

1. **Install Requirements**
   ```bash
   pip install -r backend/requirements.txt
   ```
2. **Generate Data & Train Model**
   ```bash
   python scripts/generate_data.py
   python scripts/train_model.py
   ```
3. **Start Backend API**
   ```bash
   uvicorn backend.main:app --reload
   ```
4. **Serve Frontend**
   Use any local web server in the `frontend` folder, e.g., `npx serve frontend` or `python -m http.server -d frontend`.
