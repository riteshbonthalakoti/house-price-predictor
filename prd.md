# PRD — House Price Predictor (Live Demo)

## 1. Goal
A publicly deployed, full-stack ML demo for a 100–200 person online student session. Not a notebook, not a script — an actual working product: generate data → train model → serve via API → rich UI → live public URL. The build process itself is also a teaching artifact (students see real ML engineering, not just theory).

## 2. Scope (locked)
- **Use case**: House price prediction (regression)
- **Data**: Synthetically generated (controllable, no licensing/cleaning overhead, fast)
- **Model**: Linear Regression (scikit-learn) — matches the theory segment exactly
- **Backend**: FastAPI, wrapping the trained model, exposes `/predict` and `/health`
- **Model hosting**: Hugging Face (Space or Model Hub, backend calls into it or loads it directly at startup — decide in build)
- **Frontend**: Rich dashboard, designed in Stitch, built in Antigravity — not a bare form
- **Deployment**: Cloudflare (frontend on Pages; backend reachable publicly — via HF Space endpoint or Cloudflare Worker proxying to it)
- **Source control**: GitHub, proper structure, CI running tests on push

## 3. Non-goals (explicitly out of scope for today, keeps you from scope-creeping mid-build)
- No user auth / accounts
- No database — predictions are stateless, not stored
- No multi-model comparison — Linear Regression only, on purpose (matches theory)
- No mobile app — responsive web only

## 4. Data spec
Synthetic dataset, generated once and saved as `data/house_prices.csv`, ~200–500 rows for a model that's demonstrably well-fit (small dataset is fine and honest to show — mention this to students as an intentional teaching choice, not a limitation).

Features:
| Feature | Type | Range/notes |
|---|---|---|
| size_sqft | float | 500–4000 |
| bedrooms | int | 1–6 |
| bathrooms | int | 1–4 |
| age_years | int | 0–40 |
| location_score | int | 1–10 (proxy for neighborhood desirability) |
| price_lakhs | float (target) | derived via a linear formula + gaussian noise |

## 5. Model spec
- scikit-learn `LinearRegression`, trained on the above features
- Train/test split 80/20, `random_state=42`
- Metrics tracked: MAE, RMSE, R² — printed at train time and ideally surfaced somewhere in the UI/API (nice touch: `/health` or `/model-info` endpoint returns these)
- Artifact saved as `model.pkl` (+ `feature_names.json`), pushed to Hugging Face

## 6. Backend API spec (FastAPI)
- `POST /predict` — body: `{size_sqft, bedrooms, bathrooms, age_years, location_score}` → returns `{predicted_price_lakhs, model_confidence_note}`
- `GET /health` — returns status + whether model loaded successfully
- `GET /model-info` — returns metrics (MAE/RMSE/R²) and feature importances/coefficients — genuinely useful for a student audience to see live
- CORS enabled for the Cloudflare-hosted frontend origin
- Input validation via Pydantic (reject missing/out-of-range values with clear errors — good teaching moment, matches "production-grade" framing from earlier)

## 7. Frontend spec (rich dashboard — Stitch-designed)
Screens/sections to design in Stitch, then implement:
1. **Hero/input panel** — sliders or clean number inputs for all 5 features, a prominent "Predict" action
2. **Prediction result panel** — large, animated reveal of predicted price, feels premium not just a number dump
3. **Model insight panel** — a simple chart showing how each feature contributes (e.g. bar chart of coefficients) — ties directly back to the "y = mx + b, here's what the model learned" theory beat
4. **Live scatter/fit visual** (stretch, if time allows) — the training data points with the model's fit line, the exact visual from your theory segment, now live in the product
5. Clean modern aesthetic — this is the part where Stitch does the heavy lifting; direct it toward something that reads "next-level," not templated Bootstrap-y

## 8. Deployment spec
- Frontend → Cloudflare Pages, public URL
- Backend → reachable publicly (HF Space with FastAPI, or backend on HF + Cloudflare Worker as a thin public proxy — we'll decide exact routing once we're in the IDE and can check what's actually configured)
- GitHub repo as source of truth, deploys triggered from it

## 9. Success criteria for today
- [ ] Public URL works, load time is fast, no visible errors
- [ ] A prediction can be made live, on stage, in under 10 seconds end-to-end
- [ ] UI looks distinctly non-templated — this is a deliberate flex, not just "functional"
- [ ] Repo is clean, pushed, with README a student could learn from
- [ ] You can explain every layer (data → model → API → UI → deploy) in one sentence each, live, without notes

## 10. Build order (high level — matches how we'll issue prompts)
1. **Verify all CLIs are connected and authenticated** (Colab, Stitch, GitHub, Cloudflare, Hugging Face) — nothing else starts until this is confirmed
2. Scaffold repo structure + generate synthetic dataset
3. Train model (via Colab CLI) + save artifact
4. Push model to Hugging Face
5. Build FastAPI backend, wire to the HF-hosted model
6. Design UI in Stitch, pull screens into Antigravity
7. Implement frontend against the FastAPI backend
8. Deploy backend (HF/Cloudflare) + frontend (Cloudflare Pages)
9. Push everything to GitHub, confirm CI green
10. End-to-end smoke test on the live public URL
