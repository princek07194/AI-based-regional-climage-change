"""
RegionalClimate XAI - Flask API entry point.
Region-aware explainable weather prediction.
"""
import os
import logging
from flask import Flask
from flask_cors import CORS
from routes.prediction import prediction_bp
from routes.model_info import model_info_bp
from routes.regions import regions_bp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)

    # Allow CORS from React dev server
    CORS(app, origins=["http://localhost:3000", "http://localhost:5173"])

    # Register blueprints
    app.register_blueprint(prediction_bp, url_prefix="/api")
    app.register_blueprint(model_info_bp, url_prefix="/api")
    app.register_blueprint(regions_bp, url_prefix="/api")

    @app.route("/api/health")
    def health():
        return {
            "status": "ok",
            "service": "RegionalClimate XAI Backend",
            "features": ["region-aware-prediction", "shap-explainability"],
        }

    logger.info("RegionalClimate XAI Flask app initialized")
    return app


if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
