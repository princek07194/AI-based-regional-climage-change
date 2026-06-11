"""
POST /api/predict – region-aware weather prediction with SHAP.
"""
import logging
import numpy as np
from flask import Blueprint, request, jsonify

from services.model_loader import load_model
from services.shap_service import explain_prediction
from preprocessing.feature_engineering import (
    build_feature_vector,
    WEATHER_CONDITIONS,
    get_risk_level,
)
from preprocessing.region_service import build_region_summary, validate_coordinates
from services.prediction_calibration import (
    calibrate_probabilities,
    build_top_k,
)

logger = logging.getLogger(__name__)
prediction_bp = Blueprint("prediction", __name__)

REQUIRED_WEATHER = [
    "temperature_celsius", "humidity", "wind_mph", "pressure_mb", "visibility_km",
]


def _validate_payload(data):
    if not data:
        raise ValueError("No JSON body provided")

    missing = [f for f in REQUIRED_WEATHER if f not in data]
    if missing:
        raise ValueError(f"Missing required fields: {missing}")

    if "latitude" in data and "longitude" in data:
        validate_coordinates(data["latitude"], data["longitude"])
    elif "latitude" in data or "longitude" in data:
        raise ValueError("Both latitude and longitude are required when specifying location")


@prediction_bp.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(force=True)
        _validate_payload(data)

        region_summary = build_region_summary(data)
        feature_vector = build_feature_vector(data)
        model = load_model()

        raw_class = int(model.predict(feature_vector)[0])
        raw_probabilities = model.predict_proba(feature_vector)[0]

        calibrated_probs, calibration_meta = calibrate_probabilities(raw_probabilities, data)
        predicted_class = int(np.argmax(calibrated_probs))
        confidence = float(calibrated_probs[predicted_class])
        condition = WEATHER_CONDITIONS.get(predicted_class, f"Condition {predicted_class}")
        risk = get_risk_level(predicted_class)

        top5 = build_top_k(calibrated_probs, 5)
        all_classes = [
            {
                "class": i,
                "condition": WEATHER_CONDITIONS.get(i, f"Condition {i}"),
                "probability": round(float(calibrated_probs[i]) * 100, 2),
            }
            for i in range(len(calibrated_probs))
        ]

        raw_condition = WEATHER_CONDITIONS.get(raw_class, f"Condition {raw_class}")

        feature_names = list(model.feature_names_in_)
        shap_result = explain_prediction(
            model, feature_vector, feature_names, predicted_class, region_summary
        )

        return jsonify({
            "prediction": {
                "class": predicted_class,
                "condition": condition,
                "confidence": round(confidence * 100, 2),
                "risk": risk,
                "top3": top5[:3],
                "top5": top5,
                "probability_distribution": all_classes,
                "raw_model": {
                    "class": raw_class,
                    "condition": raw_condition,
                    "confidence": round(float(raw_probabilities[raw_class]) * 100, 2),
                },
                "calibration": calibration_meta,
            },
            "explanation": shap_result,
            "region": region_summary,
            "input_summary": {
                "temperature_celsius": data.get("temperature_celsius"),
                "humidity": data.get("humidity"),
                "wind_mph": data.get("wind_mph"),
                "pressure_mb": data.get("pressure_mb"),
                "visibility_km": data.get("visibility_km"),
                "precip_mm": data.get("precip_mm", 0),
                "cloud": data.get("cloud", 50),
                "latitude": region_summary["latitude"],
                "longitude": region_summary["longitude"],
                "country": region_summary.get("country"),
                "state": region_summary.get("state"),
                "city": region_summary.get("city"),
                "climate_zone": region_summary.get("climate_zone"),
            },
        })

    except ValueError as ve:
        logger.warning(f"Validation error: {ve}")
        return jsonify({"error": str(ve)}), 422
    except FileNotFoundError as fe:
        logger.error(str(fe))
        return jsonify({"error": "Model file not found. Place weather_prediction_model.pkl in model_store/"}), 503
    except Exception as e:
        logger.error(f"Prediction failed: {e}", exc_info=True)
        return jsonify({"error": "Internal prediction error", "detail": str(e)}), 500
