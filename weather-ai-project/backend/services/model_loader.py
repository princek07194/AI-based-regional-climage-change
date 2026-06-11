"""
services/model_loader.py
Responsible for loading and caching the XGBoost model safely.
"""
import os
import pickle
import logging
import warnings
import numpy as np

logger = logging.getLogger(__name__)

# Suppress XGBoost version serialization warnings
warnings.filterwarnings("ignore", category=UserWarning, module="xgboost")

# ── paths ──────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'model_store', 'weather_prediction_model.pkl')

# ── singleton cache ────────────────────────────────────────────────────
_model = None


def load_model():
    """Load (or return cached) XGBoost model."""
    global _model
    if _model is not None:
        return _model

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found at: {MODEL_PATH}")

    logger.info(f"Loading model from {MODEL_PATH} …")
    with open(MODEL_PATH, 'rb') as f:
        _model = pickle.load(f)
    logger.info("Model loaded successfully – "
                f"classes={_model.n_classes_}, features={_model.n_features_in_}")
    return _model


def get_model_metadata():
    """Return a dict of model metadata for the /model-info endpoint."""
    model = load_model()
    booster = model.get_booster()
    scores  = booster.get_fscore()

    # Sort features by importance
    sorted_feats = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top_features = [{"feature": k, "importance": round(v, 2)} for k, v in sorted_feats[:15]]

    return {
        "model_name": "RegionalClimate XAI – XGBoost Classifier",
        "algorithm": "XGBoost (eXtreme Gradient Boosting)",
        "objective": model.objective,
        "n_estimators": model.n_estimators,
        "max_depth": model.max_depth,
        "learning_rate": model.learning_rate,
        "n_features": int(model.n_features_in_),
        "n_classes": int(model.n_classes_),
        "feature_names": list(model.feature_names_in_),
        "top_features": top_features,
        "xai_enabled": True,
        "prediction_type": "Multi-class Weather Condition Classification",
        "dataset_info": {
            "features": 30,
            "description": "Global weather readings with latitude/longitude for "
                           "region-aware classification. Includes air quality and UV.",
            "region_aware": True,
        }
    }
