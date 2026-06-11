# RegionalClimate XAI – Region-Aware Explainable Weather Prediction

Full-stack AI platform: **XGBoost** weather classification with **SHAP** explanations and **region-aware** inputs (latitude, longitude, climate zone).

---

## Project Structure

```
weather-ai-project/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── model_store/
│   │   └── weather_prediction_model.pkl   ← required
│   ├── preprocessing/
│   │   ├── feature_engineering.py
│   │   └── region_service.py
│   ├── routes/
│   │   ├── prediction.py
│   │   ├── model_info.py
│   │   └── regions.py
│   └── services/
│       ├── model_loader.py
│       └── shap_service.py
└── frontend/
    ├── src/
    │   ├── App.jsx
    │   ├── components/
    │   │   ├── layout/Hero.jsx
    │   │   ├── regional/RegionalInfo.jsx, RegionComparison.jsx
    │   │   ├── weather/WeatherParameters.jsx
    │   │   ├── prediction/PredictionResult.jsx, WeatherClassesGrid.jsx
    │   │   ├── shap/ShapExplanation.jsx
    │   │   ├── model/ModelInfoSection.jsx
    │   │   └── ui/
    │   └── utils/
    └── package.json
```

---

## Setup & Run

### 1. Model file

Place your trained model at:

`backend/model_store/weather_prediction_model.pkl`

### 2. Backend

```powershell
cd weather-ai-project/backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

→ http://localhost:5000

### 3. Frontend

```powershell
cd weather-ai-project/frontend
npm install
npm run dev
```

→ http://localhost:3000

---

## API

### `POST /api/predict`

**Required:** `temperature_celsius`, `humidity`, `wind_mph`, `pressure_mb`, `visibility_km`

**Regional (recommended):** `latitude`, `longitude`, `country`, `state`, `city`, `climate_zone`

**Optional:** `precip_mm`, `cloud`, `feels_like_celsius`

Returns: prediction (top5, all class probabilities), SHAP explanation with regional analysis, region summary.

### `GET /api/regions`

Country / state / city catalog with coordinates.

### `GET /api/model-info`

Model metadata and feature importance.

---

## Region-aware behaviour

- **Latitude & longitude** are model features (not hardcoded).
- **UV, air quality, wind direction** are derived from coordinates.
- Same temperature at **Srinagar (34°N)** vs **Jaipur (27°N)** produces different feature vectors and predictions.

---

## Tech Stack

| Layer | Stack |
|-------|--------|
| Frontend | React 18, Vite, Tailwind, Recharts |
| Backend | Flask 3, Flask-CORS |
| ML | XGBoost, scikit-learn |
| XAI | SHAP TreeExplainer |
