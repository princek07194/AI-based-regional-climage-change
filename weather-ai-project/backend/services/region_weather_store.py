import os
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / 'region_weather.db'

DEFAULT_REGION_WEATHER = [
    {
        'country': 'India', 'state': 'Jammu and Kashmir', 'city': 'Srinagar',
        'latitude': 34.08, 'longitude': 74.8, 'climate_zone': 'Cold / Alpine',
        'temperature_celsius': 15.0, 'humidity': 55.0, 'wind_mph': 8.0,
        'pressure_mb': 1012.0, 'visibility_km': 12.0, 'precip_mm': 0.0, 'cloud': 45.0,
    },
    {
        'country': 'India', 'state': 'Rajasthan', 'city': 'Jaipur',
        'latitude': 26.91, 'longitude': 75.79, 'climate_zone': 'Hot & Arid (Arid)',
        'temperature_celsius': 38.0, 'humidity': 25.0, 'wind_mph': 16.0,
        'pressure_mb': 1002.0, 'visibility_km': 8.0, 'precip_mm': 0.0, 'cloud': 15.0,
    },
    {
        'country': 'India', 'state': 'Rajasthan', 'city': 'Jodhpur',
        'latitude': 26.24, 'longitude': 73.02, 'climate_zone': 'Hot & Arid (Arid)',
        'temperature_celsius': 38.0, 'humidity': 25.0, 'wind_mph': 16.0,
        'pressure_mb': 1002.0, 'visibility_km': 8.0, 'precip_mm': 0.0, 'cloud': 15.0,
    },
    {
        'country': 'India', 'state': 'Rajasthan', 'city': 'Udaipur',
        'latitude': 24.59, 'longitude': 73.71, 'climate_zone': 'Hot & Arid (Arid)',
        'temperature_celsius': 38.0, 'humidity': 25.0, 'wind_mph': 16.0,
        'pressure_mb': 1002.0, 'visibility_km': 8.0, 'precip_mm': 0.0, 'cloud': 15.0,
    },
    {
        'country': 'India', 'state': 'Maharashtra', 'city': 'Mumbai',
        'latitude': 19.08, 'longitude': 72.88, 'climate_zone': 'Tropical Wet & Dry',
        'temperature_celsius': 30.0, 'humidity': 65.0, 'wind_mph': 11.0,
        'pressure_mb': 1008.0, 'visibility_km': 10.0, 'precip_mm': 0.0, 'cloud': 50.0,
    },
    {
        'country': 'India', 'state': 'Maharashtra', 'city': 'Pune',
        'latitude': 18.52, 'longitude': 73.86, 'climate_zone': 'Tropical Wet & Dry',
        'temperature_celsius': 30.0, 'humidity': 65.0, 'wind_mph': 11.0,
        'pressure_mb': 1008.0, 'visibility_km': 10.0, 'precip_mm': 0.0, 'cloud': 50.0,
    },
    {
        'country': 'India', 'state': 'Kerala', 'city': 'Kochi',
        'latitude': 9.93, 'longitude': 76.27, 'climate_zone': 'Tropical Monsoon',
        'temperature_celsius': 29.5, 'humidity': 85.0, 'wind_mph': 9.0,
        'pressure_mb': 1010.0, 'visibility_km': 9.0, 'precip_mm': 0.0, 'cloud': 70.0,
    },
    {
        'country': 'India', 'state': 'Kerala', 'city': 'Thiruvananthapuram',
        'latitude': 8.52, 'longitude': 76.94, 'climate_zone': 'Tropical Monsoon',
        'temperature_celsius': 29.5, 'humidity': 85.0, 'wind_mph': 9.0,
        'pressure_mb': 1010.0, 'visibility_km': 9.0, 'precip_mm': 0.0, 'cloud': 70.0,
    },
    {
        'country': 'India', 'state': 'Delhi', 'city': 'New Delhi',
        'latitude': 28.61, 'longitude': 77.21, 'climate_zone': 'Semi-Arid / Polluted',
        'temperature_celsius': 33.0, 'humidity': 45.0, 'wind_mph': 12.0,
        'pressure_mb': 1005.0, 'visibility_km': 4.0, 'precip_mm': 0.0, 'cloud': 30.0,
    },
    {
        'country': 'India', 'state': 'Karnataka', 'city': 'Bengaluru',
        'latitude': 12.97, 'longitude': 77.59, 'climate_zone': 'Tropical Savanna',
        'temperature_celsius': 27.0, 'humidity': 60.0, 'wind_mph': 10.0,
        'pressure_mb': 1011.0, 'visibility_km': 11.0, 'precip_mm': 0.0, 'cloud': 40.0,
    },
    {
        'country': 'India', 'state': 'Tamil Nadu', 'city': 'Chennai',
        'latitude': 13.08, 'longitude': 80.27, 'climate_zone': 'Tropical Maritime',
        'temperature_celsius': 32.0, 'humidity': 70.0, 'wind_mph': 13.0,
        'pressure_mb': 1008.0, 'visibility_km': 10.0, 'precip_mm': 0.0, 'cloud': 50.0,
    },
    {
        'country': 'India', 'state': 'West Bengal', 'city': 'Kolkata',
        'latitude': 22.57, 'longitude': 88.36, 'climate_zone': 'Humid Subtropical',
        'temperature_celsius': 34.5, 'humidity': 76.0, 'wind_mph': 14.0,
        'pressure_mb': 1006.0, 'visibility_km': 10.0, 'precip_mm': 0.0, 'cloud': 60.0,
    },
    {
        'country': 'United States', 'state': 'California', 'city': 'Los Angeles',
        'latitude': 34.05, 'longitude': -118.24, 'climate_zone': 'Mediterranean',
        'temperature_celsius': 25.0, 'humidity': 60.0, 'wind_mph': 8.0,
        'pressure_mb': 1014.0, 'visibility_km': 10.0, 'precip_mm': 0.0, 'cloud': 20.0,
    },
    {
        'country': 'United States', 'state': 'California', 'city': 'San Francisco',
        'latitude': 37.77, 'longitude': -122.42, 'climate_zone': 'Mediterranean',
        'temperature_celsius': 18.0, 'humidity': 75.0, 'wind_mph': 10.0,
        'pressure_mb': 1016.0, 'visibility_km': 10.0, 'precip_mm': 0.0, 'cloud': 40.0,
    },
    {
        'country': 'United States', 'state': 'New York', 'city': 'New York City',
        'latitude': 40.71, 'longitude': -74.01, 'climate_zone': 'Humid Subtropical',
        'temperature_celsius': 22.0, 'humidity': 70.0, 'wind_mph': 12.0,
        'pressure_mb': 1012.0, 'visibility_km': 10.0, 'precip_mm': 0.0, 'cloud': 35.0,
    },
    {
        'country': 'United Kingdom', 'state': 'England', 'city': 'London',
        'latitude': 51.51, 'longitude': -0.13, 'climate_zone': 'Temperate Oceanic',
        'temperature_celsius': 16.0, 'humidity': 85.0, 'wind_mph': 10.0,
        'pressure_mb': 1015.0, 'visibility_km': 10.0, 'precip_mm': 0.5, 'cloud': 65.0,
    },
]

CREATE_TABLE_SQL = '''
CREATE TABLE IF NOT EXISTS region_weather (
    country TEXT NOT NULL,
    state TEXT NOT NULL,
    city TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    climate_zone TEXT,
    temperature_celsius REAL,
    humidity REAL,
    wind_mph REAL,
    pressure_mb REAL,
    visibility_km REAL,
    precip_mm REAL,
    cloud REAL,
    PRIMARY KEY (country, state, city)
);
'''

INSERT_SQL = '''
INSERT OR REPLACE INTO region_weather (
    country, state, city, latitude, longitude, climate_zone,
    temperature_celsius, humidity, wind_mph, pressure_mb,
    visibility_km, precip_mm, cloud
) VALUES (
    :country, :state, :city, :latitude, :longitude, :climate_zone,
    :temperature_celsius, :humidity, :wind_mph, :pressure_mb,
    :visibility_km, :precip_mm, :cloud
);
'''

SELECT_SQL = '''
SELECT country, state, city, latitude, longitude, climate_zone,
       temperature_celsius, humidity, wind_mph, pressure_mb,
       visibility_km, precip_mm, cloud
FROM region_weather
WHERE lower(country) = lower(:country)
  AND lower(state) = lower(:state)
  AND lower(city) = lower(:city)
LIMIT 1;
'''


def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(CREATE_TABLE_SQL)
    conn.commit()

    cursor.executemany(INSERT_SQL, DEFAULT_REGION_WEATHER)
    conn.commit()
    conn.close()


def get_region_weather(country: str, state: str, city: str):
    if not country or not state or not city:
        return None
    ensure_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(SELECT_SQL, {
        'country': country.strip(),
        'state': state.strip(),
        'city': city.strip(),
    })
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    return dict(row)
