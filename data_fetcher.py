"""
data_fetcher.py — VAYU AI
All API calls for live and historical data. NO FAKE DATA.
APIs: Nominatim, OpenAQ, Open-Meteo, NASA FIRMS, WAQI, ip-api
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TIMEOUT = 12
HEADERS = {"User-Agent": "VAYU-AI/1.0 (hackathon project; contact@vayuai.in)"}


# ─── AUTO LOCATION (IP-based) ─────────────────────────────────────────────────
def get_user_location() -> dict:
    """Auto-detect user city and coordinates via IP geolocation."""
    try:
        resp = requests.get("http://ip-api.com/json/?fields=city,lat,lon,regionName,country", timeout=TIMEOUT)
        data = resp.json()
        if data.get("city"):
            return {
                "city": data["city"],
                "lat": float(data["lat"]),
                "lon": float(data["lon"]),
                "region": data.get("regionName", ""),
                "country": data.get("country", ""),
            }
    except Exception as e:
        logger.warning(f"IP geolocation error: {e}")
    return None


# ─── GEOCODING ─────────────────────────────────────────────────────────────────
def get_coordinates(city: str) -> tuple:
    """Convert city name to (lat, lon, display_name) using Nominatim OSM."""
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {"q": city, "format": "json", "limit": 1, "addressdetails": 1}
        resp = requests.get(url, params=params, headers=HEADERS, timeout=TIMEOUT)
        data = resp.json()
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"]), data[0]["display_name"]
    except Exception as e:
        logger.warning(f"Nominatim error for {city}: {e}")
    return None, None, None


def search_locations(query: str, limit: int = 8) -> list:
    """Search for locations globally."""
    if not query or len(query) < 2:
        return []
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {"q": query, "format": "json", "limit": limit, "addressdetails": 1, "dedupe": 1}
        resp = requests.get(url, params=params, headers=HEADERS, timeout=TIMEOUT)
        data = resp.json()
        results = []
        for item in data:
            addr = item.get("addressdetails", {})
            display = item.get("display_name", query)
            parts = display.split(",")
            short_name = ", ".join(p.strip() for p in parts[:3])
            results.append({
                "name": short_name,
                "full_name": display,
                "lat": float(item["lat"]),
                "lon": float(item["lon"]),
                "type": item.get("type", "city").replace("_", " ").title(),
                "country": addr.get("country", ""),
                "state": addr.get("state", ""),
            })
        return results
    except Exception as e:
        logger.warning(f"Location search error: {e}")
        return []


# ─── OPENAQ ────────────────────────────────────────────────────────────────────
def get_openaq_data(lat: float, lon: float, radius_km: int = 50) -> dict:
    """Fetch latest air quality readings from OpenAQ v2."""
    try:
        url = "https://api.openaq.org/v2/latest"
        params = {
            "coordinates": f"{lat},{lon}",
            "radius": radius_km * 1000,
            "limit": 30,
            "parameter": ["pm25", "pm10", "no2", "co"],
        }
        resp = requests.get(url, params=params, timeout=TIMEOUT)
        data = resp.json()
        results = data.get("results", [])

        readings = {"pm25": [], "pm10": [], "no2": [], "co": []}
        for station in results:
            for m in station.get("measurements", []):
                param = m.get("parameter", "").lower().replace(".", "")
                val = m.get("value", None)
                if val is not None and val >= 0 and param in readings:
                    readings[param].append(val)

        def avg(lst):
            return round(float(np.mean(lst)), 2) if lst else None

        pm25 = avg(readings["pm25"])
        pm10 = avg(readings["pm10"])
        no2 = avg(readings["no2"])
        co = avg(readings["co"])

        if pm25 is None and pm10 is None:
            return None

        aqi = pm25_to_aqi(pm25) if pm25 else None

        return {
            "pm25": pm25, "pm10": pm10, "no2": no2, "co": co,
            "aqi": aqi,
            "timestamp": datetime.now().isoformat(),
            "source": "OpenAQ",
        }
    except Exception as e:
        logger.warning(f"OpenAQ error: {e}")
        return None


def pm25_to_aqi(pm25: float) -> int:
    """Convert PM2.5 ug/m3 to AQI using US EPA standard breakpoints."""
    if pm25 is None:
        return None
    breakpoints = [
        (0.0, 12.0, 0, 50),
        (12.1, 35.4, 51, 100),
        (35.5, 55.4, 101, 150),
        (55.5, 150.4, 151, 200),
        (150.5, 250.4, 201, 300),
        (250.5, 350.4, 301, 400),
        (350.5, 500.4, 401, 500),
    ]
    for lo_c, hi_c, lo_i, hi_i in breakpoints:
        if lo_c <= pm25 <= hi_c:
            aqi = ((hi_i - lo_i) / (hi_c - lo_c)) * (pm25 - lo_c) + lo_i
            return int(round(aqi))
    return 500 if pm25 > 500 else 0


# ─── WAQI ──────────────────────────────────────────────────────────────────────
def get_waqi_data(city: str, token: str = "demo") -> dict:
    """Fetch AQI from WAQI by city name."""
    try:
        url = f"https://api.waqi.info/feed/{city}/"
        resp = requests.get(url, params={"token": token}, timeout=TIMEOUT)
        data = resp.json()
        if data.get("status") == "ok":
            d = data["data"]
            iaqi = d.get("iaqi", {})
            return {
                "pm25": iaqi.get("pm25", {}).get("v"),
                "pm10": iaqi.get("pm10", {}).get("v"),
                "no2": iaqi.get("no2", {}).get("v"),
                "co": iaqi.get("co", {}).get("v"),
                "aqi": d.get("aqi"),
                "timestamp": datetime.now().isoformat(),
                "source": "WAQI",
            }
    except Exception as e:
        logger.warning(f"WAQI city error: {e}")
    return None


def get_waqi_geo_data(lat: float, lon: float, token: str = "demo") -> dict:
    """Fetch AQI from WAQI by geo coordinates — most reliable method."""
    try:
        url = f"https://api.waqi.info/feed/geo:{lat};{lon}/"
        resp = requests.get(url, params={"token": token}, timeout=TIMEOUT)
        data = resp.json()
        if data.get("status") == "ok":
            d = data["data"]
            iaqi = d.get("iaqi", {})
            # Extract the real station name from the URL or city name
            raw_name = d.get("city", {}).get("name", "")
            # The station URL often has the real city name
            station_url = d.get("city", {}).get("url", "")
            # Use a cleaner source label
            return {
                "pm25": iaqi.get("pm25", {}).get("v"),
                "pm10": iaqi.get("pm10", {}).get("v"),
                "no2": iaqi.get("no2", {}).get("v"),
                "co": iaqi.get("co", {}).get("v"),
                "aqi": d.get("aqi"),
                "timestamp": datetime.now().isoformat(),
                "source": "WAQI",
            }
    except Exception as e:
        logger.warning(f"WAQI geo error: {e}")
    return None


def get_best_aqi_data(city: str, lat: float, lon: float, waqi_token: str = "demo") -> dict:
    """Try multiple sources: WAQI-geo first (most reliable), then WAQI-city, then OpenAQ."""
    # Method 1: WAQI by geo-coordinates (most reliable for any location globally)
    data = get_waqi_geo_data(lat, lon, waqi_token)
    if data and data.get("aqi"):
        return data
    # Method 2: WAQI by city name
    data = get_waqi_data(city, waqi_token)
    if data and data.get("aqi"):
        return data
    # Method 3: OpenAQ (patchy coverage in India)
    data = get_openaq_data(lat, lon)
    if data and data.get("aqi"):
        return data
    return None


# ─── OPEN-METEO FORECAST ───────────────────────────────────────────────────────
def get_weather_forecast(lat: float, lon: float) -> dict:
    """Fetch 72-hour weather forecast."""
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat, "longitude": lon,
            "hourly": "temperature_2m,relativehumidity_2m,windspeed_10m,precipitation",
            "forecast_days": 3, "timezone": "Asia/Kolkata",
        }
        resp = requests.get(url, params=params, timeout=TIMEOUT)
        data = resp.json()
        hourly = data.get("hourly", {})
        if not hourly.get("time"):
            return None
        return {
            "windspeed_10m": hourly.get("windspeed_10m", []),
            "temperature_2m": hourly.get("temperature_2m", []),
            "relativehumidity_2m": hourly.get("relativehumidity_2m", []),
            "precipitation": hourly.get("precipitation", []),
            "times": hourly.get("time", []),
        }
    except Exception as e:
        logger.warning(f"Open-Meteo forecast error: {e}")
        return None


# ─── OPEN-METEO HISTORICAL ─────────────────────────────────────────────────────
def get_historical_weather(lat: float, lon: float, days: int = 30) -> pd.DataFrame:
    """Fetch last N days of hourly weather data."""
    try:
        end = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
        start = (datetime.now() - timedelta(days=days + 5)).strftime("%Y-%m-%d")
        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            "latitude": lat, "longitude": lon,
            "start_date": start, "end_date": end,
            "hourly": "temperature_2m,relativehumidity_2m,windspeed_10m,precipitation",
            "timezone": "Asia/Kolkata",
        }
        resp = requests.get(url, params=params, timeout=15)
        data = resp.json()
        hourly = data.get("hourly", {})
        df = pd.DataFrame(hourly)
        if "time" in df.columns:
            df["time"] = pd.to_datetime(df["time"])
        return df
    except Exception as e:
        logger.warning(f"Open-Meteo historical error: {e}")
        return pd.DataFrame()


# ─── NASA FIRMS ────────────────────────────────────────────────────────────────
def get_nasa_fires(lat: float, lon: float, days: int = 2, api_key: str = "DEMO_KEY") -> pd.DataFrame:
    """Fetch active fire data from NASA FIRMS."""
    try:
        min_lat, max_lat = lat - 2.0, lat + 2.0
        min_lon, max_lon = lon - 2.0, lon + 2.0
        area = f"{min_lon},{min_lat},{max_lon},{max_lat}"
        url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{api_key}/VIIRS_SNPP_NRT/{area}/{days}"
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200 and len(resp.text) > 50:
            from io import StringIO
            df = pd.read_csv(StringIO(resp.text))
            if "latitude" in df.columns and "longitude" in df.columns:
                df["distance_km"] = df.apply(
                    lambda r: haversine(lat, lon, r["latitude"], r["longitude"]), axis=1
                )
                return df[df["distance_km"] <= 300].reset_index(drop=True)
    except Exception as e:
        logger.warning(f"NASA FIRMS error: {e}")
    return pd.DataFrame()


def haversine(lat1, lon1, lat2, lon2) -> float:
    """Calculate distance in km between two GPS points."""
    R = 6371.0
    phi1, phi2 = np.radians(lat1), np.radians(lat2)
    dphi = np.radians(lat2 - lat1)
    dlambda = np.radians(lon2 - lon1)
    a = np.sin(dphi / 2) ** 2 + np.cos(phi1) * np.cos(phi2) * np.sin(dlambda / 2) ** 2
    return 2 * R * np.arctan2(np.sqrt(a), np.sqrt(1 - a))


# ─── MULTI-CITY ────────────────────────────────────────────────────────────────
def get_multi_city_data(cities: list, waqi_token: str = "demo") -> list:
    """Fetch AQI data for multiple cities. Only returns cities with real data."""
    results = []
    for city in cities:
        time.sleep(0.3)
        lat, lon, display = get_coordinates(city)
        if lat is None:
            continue
        data = get_best_aqi_data(city, lat, lon, waqi_token)
        if data is None:
            continue
        data["city_name"] = city
        data["lat"] = lat
        data["lon"] = lon
        results.append(data)
    return results
