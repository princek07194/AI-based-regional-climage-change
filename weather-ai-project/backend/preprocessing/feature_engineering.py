"""
Maps user weather + regional inputs to the 30-feature vector expected by the XGBoost model.
"""
import datetime
import numpy as np
from preprocessing.region_service import (
    DEFAULT_LAT,
    DEFAULT_LON,
    derive_regional_defaults,
    validate_coordinates,
)

WEATHER_CONDITIONS = {
    0:  "Sunny",
    1:  "Clear",
    2:  "Partly Cloudy",
    3:  "Cloudy",
    4:  "Overcast",
    5:  "Mist",
    6:  "Patchy Rain Possible",
    7:  "Patchy Snow Possible",
    8:  "Patchy Sleet Possible",
    9:  "Patchy Freezing Drizzle Possible",
    10: "Thundery Outbreaks Possible",
    11: "Blowing Snow",
    12: "Blizzard",
    13: "Fog",
    14: "Freezing Fog",
    15: "Patchy Light Drizzle",
    16: "Light Drizzle",
    17: "Freezing Drizzle",
    18: "Heavy Freezing Drizzle",
    19: "Patchy Light Rain",
    20: "Light Rain",
    21: "Moderate Rain at Times",
    22: "Moderate Rain",
    23: "Heavy Rain at Times",
    24: "Heavy Rain",
    25: "Light Freezing Rain",
    26: "Moderate or Heavy Freezing Rain",
    27: "Light Sleet",
    28: "Moderate or Heavy Sleet",
    29: "Patchy Light Snow",
    30: "Light Snow",
    31: "Patchy Moderate Snow",
    32: "Moderate Snow",
    33: "Patchy Heavy Snow",
    34: "Heavy Snow",
    35: "Ice Pellets",
    36: "Light Rain Shower",
    37: "Moderate or Heavy Rain Shower",
    38: "Torrential Rain Shower",
    39: "Light Sleet Showers",
    40: "Moderate or Heavy Sleet Showers",
    41: "Light Snow Showers",
    42: "Moderate or Heavy Snow Showers",
    43: "Light Showers of Ice Pellets",
    44: "Moderate or Heavy Showers of Ice Pellets",
    45: "Patchy Light Rain with Thunder",
    46: "Moderate or Heavy Rain with Thunder",
    47: "Patchy Light Snow with Thunder",
}

REGIONAL_FEATURE_NAMES = {"latitude", "longitude"}

MOON_DEFAULT = 50.0


def get_risk_level(class_idx):
    if class_idx in range(0, 6):
        return {"level": "Low", "color": "green", "icon": "✅"}
    elif class_idx in range(6, 14):
        return {"level": "Moderate", "color": "yellow", "icon": "⚠️"}
    elif class_idx in range(14, 30):
        return {"level": "High", "color": "orange", "icon": "🌧️"}
    return {"level": "Severe", "color": "red", "icon": "⛈️"}


def celsius_to_fahrenheit(c):
    return round(c * 9 / 5 + 32, 2)


def mph_to_kph(mph):
    return round(mph * 1.60934, 2)


def km_to_miles(km):
    return round(km * 0.621371, 2)


def mb_to_in(mb):
    return round(mb * 0.0295301, 2)


def mm_to_in(mm):
    return round(mm * 0.0393701, 2)


def _derive_feels_like(temp_c, humidity, wind_mph, feels_c_override):
    if feels_c_override is not None:
        return float(feels_c_override)
    wind_kph_val = mph_to_kph(wind_mph)
    if temp_c <= 10 and wind_kph_val > 4.8:
        return (
            13.12 + 0.6215 * temp_c
            - 11.37 * (wind_kph_val ** 0.16)
            + 0.3965 * temp_c * (wind_kph_val ** 0.16)
        )
    if temp_c >= 27:
        return (
            -8.78469475556
            + 1.61139411 * temp_c
            + 2.33854883889 * humidity
            - 0.14611605 * temp_c * humidity
            - 0.012308094 * (temp_c ** 2)
            - 0.0164248277778 * (humidity ** 2)
            + 0.002211732 * (temp_c ** 2) * humidity
            + 0.00072546 * temp_c * (humidity ** 2)
            - 0.000003582 * (temp_c ** 2) * (humidity ** 2)
        )
    return temp_c


def build_feature_vector(user_input: dict) -> np.ndarray:
    """
    Build the 30-feature row. Accepts weather sliders plus optional:
    latitude, longitude (region-aware prediction).
    """
    temp_c = float(user_input.get("temperature_celsius", 25.0))
    humidity = float(user_input.get("humidity", 60.0))
    wind_mph = float(user_input.get("wind_mph", 10.0))
    pres_mb = float(user_input.get("pressure_mb", 1013.0))
    vis_km = float(user_input.get("visibility_km", 10.0))
    prec_mm = float(user_input.get("precip_mm", 0.0))
    cloud = float(user_input.get("cloud", 50.0))

    # Region: use provided coordinates or India-centre defaults
    lat_raw = user_input.get("latitude", DEFAULT_LAT)
    lon_raw = user_input.get("longitude", DEFAULT_LON)
    latitude, longitude = validate_coordinates(lat_raw, lon_raw)

    regional = derive_regional_defaults(latitude, longitude)
    feels_c = _derive_feels_like(
        temp_c, humidity, wind_mph, user_input.get("feels_like_celsius")
    )
    gust_mph = round(wind_mph * 1.25, 2)
    epoch = int(datetime.datetime.utcnow().timestamp())

    feature_vector = [
        latitude,
        longitude,
        epoch,
        temp_c,
        celsius_to_fahrenheit(temp_c),
        wind_mph,
        mph_to_kph(wind_mph),
        regional["wind_degree"],
        pres_mb,
        mb_to_in(pres_mb),
        prec_mm,
        mm_to_in(prec_mm),
        humidity,
        cloud,
        feels_c,
        celsius_to_fahrenheit(feels_c),
        vis_km,
        km_to_miles(vis_km),
        regional["uv_index"],
        gust_mph,
        mph_to_kph(gust_mph),
        regional["air_quality_Carbon_Monoxide"],
        regional["air_quality_Ozone"],
        regional["air_quality_Nitrogen_dioxide"],
        regional["air_quality_Sulphur_dioxide"],
        regional["air_quality_PM2.5"],
        regional["air_quality_PM10"],
        regional["air_quality_us-epa-index"],
        regional["air_quality_gb-defra-index"],
        MOON_DEFAULT,
    ]

    return np.array([feature_vector], dtype=np.float64)
