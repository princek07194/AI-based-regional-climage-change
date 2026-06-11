"""
Region-aware helpers: climate zones, geo validation, and location-based defaults.
Latitude/longitude feed directly into the model; other features are derived heuristically.
"""
import math

# Valid coordinate ranges
LAT_MIN, LAT_MAX = -90.0, 90.0
LON_MIN, LON_MAX = -180.0, 180.0

# Default centre of India (backward compatible)
DEFAULT_LAT = 20.0
DEFAULT_LON = 78.0


def validate_coordinates(latitude, longitude):
    """Raise ValueError if coordinates are out of range."""
    lat = float(latitude)
    lon = float(longitude)
    if not (LAT_MIN <= lat <= LAT_MAX):
        raise ValueError(f"latitude must be between {LAT_MIN} and {LAT_MAX}")
    if not (LON_MIN <= lon <= LON_MAX):
        raise ValueError(f"longitude must be between {LON_MIN} and {LON_MAX}")
    return lat, lon


def get_climate_zone(latitude, longitude=None):
    """
    Classify climate zone from latitude (India-focused bands).
    longitude reserved for future coastal/inland refinement.
    """
    lat = float(latitude)
    if lat >= 32:
        return "Alpine / Himalayan"
    if lat >= 23.5:
        return "Subtropical"
    if lat >= 15:
        return "Tropical Wet & Dry"
    return "Tropical"


def derive_regional_defaults(latitude, longitude):
    """
    Region-aware defaults for features not supplied by the user.
    Same temperature at different lat/lon yields different full feature vectors.
    """
    lat = float(latitude)
    lon = float(longitude)

    # UV: higher in southern India, moderated in north / mountains
    uv = round(max(2.0, min(11.0, 6.5 + (23.0 - abs(lat - 20.0)) * 0.12)), 1)

    # Air quality: arid west (Rajasthan/Gujarat) vs Indo-Gangetic vs mountains vs coastal
    if lat >= 32:
        pm25, pm10, co, no2 = 12.0, 22.0, 180.0, 12.0
    elif 23 <= lat <= 30 and 69 <= lon <= 76:
        # Thar / Rajasthan–Gujarat arid belt (Jaipur, Jodhpur, etc.)
        pm25, pm10, co, no2 = 18.0, 32.0, 220.0, 14.0
    elif 24 <= lat <= 31 and 77 <= lon <= 88:
        # Indo-Gangetic plain (Delhi, UP, Bihar) — not western Rajasthan
        pm25, pm10, co, no2 = 48.0, 85.0, 420.0, 35.0
    elif lon >= 72 and lon <= 78 and lat < 20:
        pm25, pm10, co, no2 = 18.0, 32.0, 260.0, 18.0
    else:
        pm25, pm10, co, no2 = 22.0, 38.0, 300.0, 20.0

    # Wind direction: monsoon-aware coarse heuristic (India)
    if 5 <= lat <= 30 and 68 <= lon <= 95:
        wind_degree = 240 if lat < 20 else 270
    else:
        wind_degree = 180

    return {
        "uv_index": uv,
        "wind_degree": wind_degree,
        "air_quality_Carbon_Monoxide": co,
        "air_quality_Ozone": round(55 + (30 - lat) * 0.3, 1),
        "air_quality_Nitrogen_dioxide": no2,
        "air_quality_Sulphur_dioxide": round(8 + pm25 * 0.05, 1),
        "air_quality_PM2.5": pm25,
        "air_quality_PM10": pm10,
        "air_quality_us-epa-index": 2 if pm25 < 25 else (3 if pm25 < 55 else 4),
        "air_quality_gb-defra-index": 2 if pm25 < 25 else (3 if pm25 < 55 else 4),
    }


def build_region_summary(data: dict) -> dict:
    """Human-readable region block for API responses."""
    lat = float(data.get("latitude", DEFAULT_LAT))
    lon = float(data.get("longitude", DEFAULT_LON))
    return {
        "country": data.get("country", ""),
        "state": data.get("state", ""),
        "city": data.get("city", ""),
        "latitude": round(lat, 4),
        "longitude": round(lon, 4),
        "climate_zone": data.get("climate_zone") or get_climate_zone(lat, lon),
        "location_label": _location_label(data),
    }


def _location_label(data: dict) -> str:
    parts = [data.get("city"), data.get("state"), data.get("country")]
    label = ", ".join(p for p in parts if p)
    if label:
        return label
    lat = data.get("latitude")
    lon = data.get("longitude")
    if lat is not None and lon is not None:
        return f"{float(lat):.2f}°N, {float(lon):.2f}°E"
    return "Unknown region"
