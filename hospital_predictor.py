"""
hospital_predictor.py — VAYU AI
Predict hospital load and preparedness based on 72-hour AQI forecast.
Formula: For every 50 AQI above 150, expect 200 extra respiratory cases per 10 lakh population.
"""

import numpy as np


# Medicines to stock based on AQI
MEDICINE_STOCK = {
    "Moderate (AQI 100-150)": [
        "Salbutamol (Albuterol) inhalers",
        "Antihistamines (Cetirizine, Loratadine)",
        "Saline nasal sprays",
        "Vitamin C supplements",
    ],
    "Unhealthy (AQI 150-200)": [
        "Salbutamol (Albuterol) inhalers — 2x normal stock",
        "Ipratropium bromide inhalers",
        "Prednisolone (oral corticosteroid)",
        "Doxophylline bronchodilators",
        "Antihistamines",
        "Oxygen concentrators — check stock",
        "Azithromycin (prevent secondary infections)",
    ],
    "Very Unhealthy (AQI 200-300)": [
        "Salbutamol inhalers — 3x stock",
        "IV Methylprednisolone",
        "Nebuliser kits",
        "Oxygen cylinders — emergency reserve",
        "Broad-spectrum antibiotics",
        "Montelukast",
        "Blood pressure medications (cardiovascular cases expected)",
        "ICU readiness for extreme cases",
    ],
    "Hazardous (AQI 300+)": [
        "All above medications — MAXIMUM stock",
        "Ventilator readiness",
        "Cardiac emergency kits",
        "Full ICU activation protocol",
        "Emergency triage staff deployment",
        "Ambulance standby increase",
    ],
}


def predict_hospital_load(
    aqi_forecast: list[int],
    population_lakhs: float = 10.0,
) -> dict:
    """
    Predict extra hospital patients for each of the 72 forecast hours.

    Formula: 
      extra_patients = (AQI - 150) / 50 * 200 * (population_lakhs / 10)
      (only when AQI > 150)
    
    Returns:
      - hourly_extra_patients: list of 72 ints
      - peak_hour_idx: hour with max load
      - total_72h_patients: cumulative extra patients
      - recommended_beds: beds to prepare
      - alert_level: str
      - medicines: list of medicines to stock
    """
    hourly_patients = []
    for aqi in aqi_forecast:
        if aqi <= 150:
            extra = 0
        else:
            factor = (aqi - 150) / 50.0
            extra = factor * 200 * (population_lakhs / 10.0)
        hourly_patients.append(max(0, int(round(extra))))

    peak_idx = int(np.argmax(hourly_patients))
    peak_patients = hourly_patients[peak_idx]
    total_72h = sum(hourly_patients)
    
    # Beds needed = peak rate * 2 hours average stay (for respiratory ER patients)
    recommended_beds = int(peak_patients * 2)

    # Alert level based on 24h max AQI
    max_aqi_24h = max(aqi_forecast[:24]) if len(aqi_forecast) >= 24 else max(aqi_forecast)

    if max_aqi_24h >= 300:
        alert_level = "EMERGENCY"
        alert_color = "#7e0023"
        medicines = MEDICINE_STOCK["Hazardous (AQI 300+)"]
    elif max_aqi_24h >= 200:
        alert_level = "CRITICAL"
        alert_color = "#8f3f97"
        medicines = MEDICINE_STOCK["Very Unhealthy (AQI 200-300)"]
    elif max_aqi_24h >= 150:
        alert_level = "HIGH"
        alert_color = "#ff0000"
        medicines = MEDICINE_STOCK["Unhealthy (AQI 150-200)"]
    elif max_aqi_24h >= 100:
        alert_level = "MODERATE"
        alert_color = "#ff7e00"
        medicines = MEDICINE_STOCK["Moderate (AQI 100-150)"]
    else:
        alert_level = "NORMAL"
        alert_color = "#00e400"
        medicines = ["Normal stock sufficient"]

    # Staff recommendations
    staff_recommendations = _get_staff_recs(alert_level, peak_patients)

    return {
        "hourly_patients": hourly_patients,
        "peak_hour_idx": peak_idx,
        "peak_patients_per_hour": peak_patients,
        "total_72h_patients": total_72h,
        "recommended_beds": recommended_beds,
        "alert_level": alert_level,
        "alert_color": alert_color,
        "medicines": medicines,
        "staff_recommendations": staff_recommendations,
        "max_aqi_24h": max_aqi_24h,
    }


def _get_staff_recs(alert_level: str, peak_patients: int) -> list[str]:
    base = [
        f"Prepare {max(1, peak_patients // 5)} additional respiratory nurses per shift",
        "Ensure nebuliser units are cleaned and ready",
        "Brief ER staff on AQI-related respiratory protocols",
    ]
    if alert_level in ("CRITICAL", "EMERGENCY"):
        base += [
            "Activate emergency respiratory care protocol",
            "Call off-duty pulmonologists for standby",
            "Coordinate with nearest government hospital for overflow",
            "Prepare mass casualty triage area",
        ]
    elif alert_level == "HIGH":
        base += [
            "Add 1 extra pulmonologist on evening shift",
            "Pre-position oxygen therapy equipment in ER",
        ]
    return base
