"""
GET /api/regions – static region metadata for the frontend dropdowns.
"""
import json
import os
import urllib.parse
import urllib.request
from urllib.error import HTTPError, URLError

from flask import Blueprint, jsonify, request
from services.region_weather_store import get_region_weather

regions_bp = Blueprint("regions", __name__)

OPENWEATHER_API_KEY = os.environ.get(
    "OPENWEATHER_API_KEY",
    "91dc593f9a58437999883952252803",
)
OPENWEATHER_ENDPOINT = "https://api.openweathermap.org/data/2.5/weather"


def _fetch_weather_from_openweather(latitude, longitude):
    if not OPENWEATHER_API_KEY:
        raise RuntimeError("OpenWeatherMap API key is not configured")

    params = urllib.parse.urlencode({
        "lat": latitude,
        "lon": longitude,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
    })
    url = f"{OPENWEATHER_ENDPOINT}?{params}"

    try:
        with urllib.request.urlopen(url, timeout=15) as response:
            payload = json.load(response)
    except HTTPError as exc:
        raise RuntimeError(f"Weather API request failed ({exc.code})") from exc
    except URLError as exc:
        raise RuntimeError(f"Weather API fetch error: {exc.reason}") from exc

    if payload.get("cod") not in (200, "200"):
        message = payload.get("message", "unknown error")
        raise RuntimeError(f"Weather API returned error: {message}")

    main = payload.get("main", {})
    wind = payload.get("wind", {})
    clouds = payload.get("clouds", {})
    rain = payload.get("rain", {})
    snow = payload.get("snow", {})

    precipitation = 0.0
    if "1h" in rain:
        precipitation = float(rain["1h"])
    elif "1h" in snow:
        precipitation = float(snow["1h"])

    return {
        "temperature_celsius": float(main.get("temp", 25.0)),
        "humidity": float(main.get("humidity", 60.0)),
        "pressure_mb": float(main.get("pressure", 1013.0)),
        "wind_mph": round(float(wind.get("speed", 4.5)) * 2.23694, 2),
        "visibility_km": round(float(payload.get("visibility", 10000)) / 1000.0, 2),
        "precip_mm": precipitation,
        "cloud": float(clouds.get("all", 0.0)),
    }


@regions_bp.route("/current-weather", methods=["GET"])
def get_current_weather_route():
    latitude = request.args.get("latitude")
    longitude = request.args.get("longitude")
    if latitude is None or longitude is None:
        return jsonify({"error": "latitude and longitude are required"}), 400

    try:
        weather = _fetch_weather_from_openweather(latitude, longitude)
    except RuntimeError as err:
        return jsonify({"error": str(err)}), 502

    return jsonify({"current_weather": weather})

# Curated dataset (extend as needed); coordinates drive model features
REGIONS = {
    "India": {
        "Jammu and Kashmir": {
            "Srinagar": {"lat": 34.08, "lon": 74.80, "climate_zone": "Alpine / Himalayan"},
            "Leh": {"lat": 34.15, "lon": 77.58, "climate_zone": "Alpine / Himalayan"},
        },
        "Rajasthan": {
            "Jaipur": {"lat": 26.91, "lon": 75.79, "climate_zone": "Subtropical"},
            "Jodhpur": {"lat": 26.24, "lon": 73.02, "climate_zone": "Subtropical"},
            "Udaipur": {"lat": 24.59, "lon": 73.71, "climate_zone": "Subtropical"},
        },
        "Maharashtra": {
            "Mumbai": {"lat": 19.08, "lon": 72.88, "climate_zone": "Tropical Wet & Dry"},
            "Pune": {"lat": 18.52, "lon": 73.86, "climate_zone": "Tropical Wet & Dry"},
        },
        "Kerala": {
            "Kochi": {"lat": 9.93, "lon": 76.27, "climate_zone": "Tropical"},
            "Thiruvananthapuram": {"lat": 8.52, "lon": 76.94, "climate_zone": "Tropical"},
        },
        "Delhi": {
            "New Delhi": {"lat": 28.61, "lon": 77.21, "climate_zone": "Subtropical"},
        },
        "Punjab": {
            "Amritsar": {"lat": 31.63, "lon": 74.87, "climate_zone": "Subtropical"},
            "Chandigarh": {"lat": 30.74, "lon": 76.79, "climate_zone": "Subtropical"},
        },
        "Uttar Pradesh": {
            "Lucknow": {"lat": 26.85, "lon": 80.95, "climate_zone": "Humid Subtropical"},
            "Varanasi": {"lat": 25.32, "lon": 82.99, "climate_zone": "Humid Subtropical"},
        },
        "Bihar": {
            "Patna": {"lat": 25.61, "lon": 85.14, "climate_zone": "Humid Subtropical"},
            "Gaya": {"lat": 24.79, "lon": 84.99, "climate_zone": "Humid Subtropical"},
        },
        "Karnataka": {
            "Bengaluru": {"lat": 12.97, "lon": 77.59, "climate_zone": "Tropical Wet & Dry"},
        },
        "Tamil Nadu": {
            "Chennai": {"lat": 13.08, "lon": 80.27, "climate_zone": "Tropical"},
        },
        "West Bengal": {
            "Kolkata": {"lat": 22.57, "lon": 88.36, "climate_zone": "Tropical Wet & Dry"},
        },
    },
    "United States": {
        "California": {
            "Los Angeles": {"lat": 34.05, "lon": -118.24, "climate_zone": "Mediterranean"},
            "San Francisco": {"lat": 37.77, "lon": -122.42, "climate_zone": "Mediterranean"},
        },
        "New York": {
            "New York City": {"lat": 40.71, "lon": -74.01, "climate_zone": "Humid Subtropical"},
        },
    },
    "United Kingdom": {
        "England": {
            "London": {"lat": 51.51, "lon": -0.13, "climate_zone": "Temperate Oceanic"},
        },
    },
}


@regions_bp.route("/regions", methods=["GET"])
def list_regions():
    countries = []
    for country, states in REGIONS.items():
        state_list = []
        for state, cities in states.items():
            city_list = [
                {
                    "name": name,
                    "latitude": info["lat"],
                    "longitude": info["lon"],
                    "climate_zone": info["climate_zone"],
                }
                for name, info in cities.items()
            ]
            state_list.append({"name": state, "cities": city_list})
        countries.append({"name": country, "states": state_list})
    return jsonify({"countries": countries})


@regions_bp.route("/region-weather", methods=["GET"])
def get_region_weather_route():
    country = request.args.get("country", "").strip()
    state = request.args.get("state", "").strip()
    city = request.args.get("city", "").strip()
    if not country or not state or not city:
        return jsonify({"error": "country, state, and city are required"}), 400

    region_weather = get_region_weather(country, state, city)
    if not region_weather:
        return jsonify({"error": "Region weather not found"}), 404

    return jsonify({"region_weather": region_weather})
