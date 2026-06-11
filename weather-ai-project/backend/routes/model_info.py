"""
routes/model_info.py
GET /api/model-info  – return model metadata and feature importance.
"""
import logging
from flask import Blueprint, jsonify
from services.model_loader import get_model_metadata

logger = logging.getLogger(__name__)
model_info_bp = Blueprint('model_info', __name__)


@model_info_bp.route('/model-info', methods=['GET'])
def model_info():
    """Return metadata, hyperparameters, and top feature importances."""
    try:
        meta = get_model_metadata()
        return jsonify(meta)
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 503
    except Exception as e:
        logger.error(f"model-info error: {e}", exc_info=True)
        return jsonify({"error": "Could not load model information"}), 500
