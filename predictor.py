"""
predictor.py — VAYU AI
72-hour AQI prediction using REAL forecast data from Open-Meteo Air Quality API.
NO FAKE DATA.
"""

import requests
import logging
from datetime import datetime, timedelta
import data_fetcher as df_mod

logger = logging.getLogger(__name__)

class VayuPredictor:
    def predict_72h(
        self,
        current_pm25: float,
        weather_forecast: dict,  # kept for signature compatibility
        fire_distance_km: float = 300.0,
        start_dt: datetime = None,
    ) -> dict:
        """
        Fetch actual 72-hour PM2.5 forecast from Open-Meteo Air Quality API.
        Returns dict with 'pm25', 'aqi', 'times', 'peak_hour_idx'.
        Returns None on failure.
        """
        if start_dt is None:
            start_dt = datetime.now()
            
        # We need the current lat/lon from session state, but we don't have it directly here.
        # Since this method is usually called after fetch_city_data, we can get it from Streamlit.
        import streamlit as st
        lat = st.session_state.get("lat")
        lon = st.session_state.get("lon")
        
        if not lat or not lon:
            return None

        try:
            url = "https://air-quality-api.open-meteo.com/v1/air-quality"
            params = {
                "latitude": lat,
                "longitude": lon,
                "hourly": "pm2_5",
                "timezone": "Asia/Kolkata",
                "forecast_days": 4  # Get 4 days to ensure we have 72 hours from current hour
            }
            resp = requests.get(url, params=params, timeout=10)
            data = resp.json()
            
            hourly = data.get("hourly", {})
            times_api = hourly.get("time", [])
            pm25_api = hourly.get("pm2_5", [])
            
            if not times_api or not pm25_api:
                return None
                
            # Filter to start from current hour and get exactly 72 hours
            current_hour_str = start_dt.strftime("%Y-%m-%dT%H:00")
            
            start_idx = 0
            for i, t in enumerate(times_api):
                if t >= current_hour_str:
                    start_idx = i
                    break
                    
            pm25_predictions = []
            aqi_predictions = []
            times = []
            
            # Use current real PM2.5 for the first reading if available, to make it seamless
            # Then blend into the API forecast
            
            for i in range(72):
                idx = start_idx + i
                if idx < len(pm25_api):
                    raw_pm25 = pm25_api[idx]
                    if raw_pm25 is None:
                        # Forward-fill: use last real value, skip if no prior value
                        raw_pm25 = pm25_predictions[-1] if pm25_predictions else None
                else:
                    raw_pm25 = pm25_predictions[-1] if pm25_predictions else None

                # Skip hours where we have no real data at all
                if raw_pm25 is None:
                    continue
                # Smooth blending for the first few hours from the current real PM2.5 reading
                if i == 0 and current_pm25 is not None:
                    pred_pm25 = current_pm25
                elif i < 6 and current_pm25 is not None:
                    weight_real = (6 - i) / 6.0
                    pred_pm25 = (current_pm25 * weight_real) + (raw_pm25 * (1 - weight_real))
                else:
                    pred_pm25 = raw_pm25
                
                # Apply exact same fire proximity scaling as before
                fire_multiplier = 1.0
                if fire_distance_km < 100:
                    fire_multiplier = 1.0 + (100 - fire_distance_km) / 200.0  # max 1.5x at 0km
                    
                pred_pm25 = pred_pm25 * fire_multiplier
                pred_pm25 = max(1.0, min(900.0, float(pred_pm25)))
                
                dt_i = start_dt + timedelta(hours=i)
                time_str = dt_i.strftime("%Y-%m-%d %H:%M")
                
                pm25_predictions.append(round(pred_pm25, 1))
                aqi_predictions.append(df_mod.pm25_to_aqi(pred_pm25))
                times.append(time_str)

            import numpy as np
            peak_idx = int(np.argmax(aqi_predictions))

            return {
                "pm25": pm25_predictions,
                "aqi": aqi_predictions,
                "times": times,
                "peak_hour_idx": peak_idx,
                "peak_aqi": aqi_predictions[peak_idx],
                "peak_time": times[peak_idx],
            }
            
        except Exception as e:
            logger.warning(f"Air Quality Forecast API error: {e}")
            return None


# Singleton
_predictor = None

def get_predictor() -> VayuPredictor:
    global _predictor
    if _predictor is None:
        _predictor = VayuPredictor()
    return _predictor
