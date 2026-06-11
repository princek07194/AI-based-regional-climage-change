"""
SHAP explanations with regional feature highlighting.
"""
import logging
import numpy as np
import shap
import warnings
from preprocessing.feature_engineering import REGIONAL_FEATURE_NAMES

warnings.filterwarnings("ignore")
logger = logging.getLogger(__name__)

_explainer = None


def get_explainer(model):
    global _explainer
    if _explainer is None:
        logger.info("Creating SHAP TreeExplainer…")
        _explainer = shap.TreeExplainer(model)
    return _explainer


def _regional_analysis(records, region_summary=None):
    """Extract SHAP contributions for geo features."""
    regional = [r for r in records if r["feature"] in REGIONAL_FEATURE_NAMES]
    regional.sort(key=lambda r: abs(r["shap_value"]), reverse=True)
    total = sum(abs(r["shap_value"]) for r in regional)
    for r in regional:
        r["is_regional"] = True
        r["contribution_pct"] = round(
            (abs(r["shap_value"]) / total * 100) if total > 0 else 0, 1
        )

    summary_parts = []
    if region_summary and region_summary.get("location_label"):
        summary_parts.append(
            f"Location context: {region_summary['location_label']} "
            f"({region_summary.get('climate_zone', 'N/A')})."
        )
    for r in regional:
        direction = "increased" if r["shap_value"] > 0 else "decreased"
        summary_parts.append(
            f"{r['feature'].replace('_', ' ')} ({r['value']}) {direction} "
            f"regional influence (SHAP {r['shap_value']:+.4f})."
        )

    return {
        "features": regional,
        "summary": " ".join(summary_parts) if summary_parts else "Minimal regional SHAP impact.",
        "total_regional_impact": round(total, 6),
    }


def explain_prediction(
    model,
    feature_vector: np.ndarray,
    feature_names: list,
    predicted_class: int,
    region_summary=None,
):
    try:
        explainer = get_explainer(model)
        shap_values = explainer.shap_values(feature_vector)
        class_shap = shap_values[0, :, predicted_class]
        base_value = float(explainer.expected_value[predicted_class])

        records = []
        for i, fname in enumerate(feature_names):
            records.append({
                "feature": fname,
                "value": round(float(feature_vector[0, i]), 4),
                "shap_value": round(float(class_shap[i]), 6),
                "impact": "positive" if class_shap[i] > 0 else "negative",
                "is_regional": fname in REGIONAL_FEATURE_NAMES,
            })

        records.sort(key=lambda r: abs(r["shap_value"]), reverse=True)
        top_positive = [r for r in records if r["shap_value"] > 0][:5]
        top_negative = [r for r in records if r["shap_value"] < 0][:5]
        regional = _regional_analysis(records, region_summary)

        pos_names = [r["feature"].replace("_", " ") for r in top_positive[:3]]
        neg_names = [r["feature"].replace("_", " ") for r in top_negative[:3]]
        nl_parts = []
        if pos_names:
            nl_parts.append(f"{', '.join(pos_names)} increased the prediction probability")
        if neg_names:
            nl_parts.append(f"{', '.join(neg_names)} reduced it")

        natural_language = (
            "Key factors: " + " while ".join(nl_parts) + ". " + regional["summary"]
            if nl_parts
            else regional["summary"]
        )

        return {
            "shap_values": records[:15],
            "top_positive": top_positive,
            "top_negative": top_negative,
            "regional_analysis": regional,
            "natural_language": natural_language.strip(),
            "base_value": round(base_value, 6),
            "prediction_delta": round(float(class_shap.sum()), 6),
        }

    except Exception as e:
        logger.error(f"SHAP failed: {e}", exc_info=True)
        return {
            "error": str(e),
            "shap_values": [],
            "top_positive": [],
            "top_negative": [],
            "regional_analysis": {"features": [], "summary": "", "total_regional_impact": 0},
            "natural_language": "Explanation unavailable for this prediction.",
        }
