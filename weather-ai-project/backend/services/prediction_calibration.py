"""
Input-driven calibration: user sliders (cloud, precip, temp) override implausible model outputs.
Works for all regions — Delhi, Rajasthan, etc.
"""
import numpy as np
from preprocessing.feature_engineering import WEATHER_CONDITIONS

# Requires freezing temperatures
FREEZING_CLASSES = {
    7, 8, 9, 11, 12, 14, 17, 18, 25, 26, 27, 28,
    29, 30, 31, 32, 33, 34, 35, 39, 40, 41, 42, 43, 44, 47,
}

# Any rain, drizzle, shower, sleet, thunder-rain, or "possible" wet weather
WET_WEATHER_CLASSES = {
    6, 8, 9, 10, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
    25, 26, 27, 28, 36, 37, 38, 39, 40, 45, 46,
}

CLOUDY_SKY_CLASSES = {3, 4}
CLEAR_SKY_CLASSES = {0, 1, 2}


def _zero_classes(probs: np.ndarray, class_ids: set) -> None:
    for i in class_ids:
        probs[i] = 0.0


def _set_distribution(length: int, weights: dict) -> np.ndarray:
    out = np.zeros(length, dtype=np.float64)
    for cls, w in weights.items():
        out[int(cls)] = float(w)
    return out


def calibrate_probabilities(probabilities: np.ndarray, user_input: dict) -> tuple:
    temp = float(user_input.get("temperature_celsius", 25))
    humidity = float(user_input.get("humidity", 60))
    precip = float(user_input.get("precip_mm", 0))
    cloud = float(user_input.get("cloud", 50))

    n = len(probabilities)
    probs = np.array(probabilities, dtype=np.float64)
    notes = []
    forced = False

    # ── Rule 1: No precipitation → no rain/drizzle/showers (ALL regions) ──
    if precip < 0.1:
        _zero_classes(probs, WET_WEATHER_CLASSES)
        notes.append("0 mm precipitation → rain/drizzle/shower classes removed")

    # ── Rule 2: Warm → no snow/ice ──
    if temp > 5:
        _zero_classes(probs, FREEZING_CLASSES)
        if temp > 5:
            notes.append(f"temp {temp}°C → snow/ice classes removed")

    # ── Rule 3: Near-zero cloud + no rain → clear sky only (Delhi, Rajasthan, anywhere) ──
    if cloud <= 10 and precip < 0.1:
        _zero_classes(probs, CLOUDY_SKY_CLASSES | WET_WEATHER_CLASSES | FREEZING_CLASSES)

        if temp >= 30:
            weights = {0: 0.48, 1: 0.34, 2: 0.16, 5: 0.02}
        elif temp >= 24:
            weights = {0: 0.38, 1: 0.36, 2: 0.22, 5: 0.04}
        else:
            weights = {1: 0.35, 2: 0.40, 0: 0.20, 5: 0.05}

        # High humidity + low cloud: allow slight mist/fog, never rain
        if humidity >= 75 and temp < 32:
            weights[5] = 0.08
            weights[0] = max(0.0, weights.get(0, 0) - 0.05)
        if humidity >= 85:
            weights[13] = 0.06
            weights[0] = max(0.0, weights.get(0, 0.1) - 0.06)

        total_w = sum(weights.values())
        weights = {k: v / total_w for k, v in weights.items()}
        probs = _set_distribution(n, weights)
        forced = True
        notes.append("0% cloud + 0 mm rain → sunny/clear forecast (all regions)")

    elif cloud <= 25 and precip < 0.1:
        _zero_classes(probs, CLOUDY_SKY_CLASSES)
        _zero_classes(probs, WET_WEATHER_CLASSES)
        for i in CLEAR_SKY_CLASSES:
            probs[i] *= 5.0
        notes.append("low cloud + dry → favouring clear conditions")

    elif cloud >= 70 and precip >= 0.5:
        for i in CLEAR_SKY_CLASSES:
            probs[i] *= 0.1
        probs[3] *= 2.0
        probs[4] *= 2.5
        for i in WET_WEATHER_CLASSES:
            probs[i] *= 1.5
        notes.append("high cloud + rain input → wet weather favoured")

    elif cloud >= 70:
        for i in CLEAR_SKY_CLASSES:
            probs[i] *= 0.2
        probs[3] *= 2.0
        probs[4] *= 2.5
        notes.append("high cloud → cloudy/overcast favoured")

    # ── Rule 4: Heavy rain input must show wet classes ──
    if precip >= 2.0:
        for i in CLEAR_SKY_CLASSES:
            probs[i] *= 0.05
        for i in WET_WEATHER_CLASSES:
            probs[i] *= 2.0
        notes.append("precipitation input supports rain")

    total = probs.sum()
    if total <= 0:
        probs = _set_distribution(n, {0: 0.45, 1: 0.35, 2: 0.20})
        forced = True
        total = probs.sum()

    calibrated = probs / total

    # Safety: never return rain as top class when user said dry + clear
    if cloud <= 10 and precip < 0.1:
        top = int(np.argmax(calibrated))
        if top in WET_WEATHER_CLASSES or top in CLOUDY_SKY_CLASSES:
            probs = _set_distribution(n, {0: 0.5, 1: 0.35, 2: 0.15})
            calibrated = probs

    meta = {
        "applied": True,
        "forced_clear_sky": forced,
        "temperature_celsius": temp,
        "humidity": humidity,
        "cloud": cloud,
        "precip_mm": precip,
        "note": "; ".join(notes),
    }
    return calibrated, meta


def build_top_k(probabilities: np.ndarray, k: int = 5):
    idx = np.argsort(probabilities)[::-1][:k]
    return [
        {
            "class": int(i),
            "condition": WEATHER_CONDITIONS.get(int(i), f"Condition {i}"),
            "probability": round(float(probabilities[i]) * 100, 2),
        }
        for i in idx
    ]
