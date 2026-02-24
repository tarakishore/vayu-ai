"""
health_calculator.py — VAYU AI
Personal health risk calculator based on user profile and current AQI.
"""

import numpy as np


# AQI health effects reference
AQI_HEALTH_MAP = {
    (0, 50): {
        "level": "Good",
        "color": "#00e400",
        "general": "Air quality is satisfactory. Enjoy outdoor activities.",
        "sensitive": "No special precautions needed.",
    },
    (51, 100): {
        "level": "Moderate",
        "color": "#ffff00",
        "general": "Acceptable air quality. Sensitive individuals may experience minor symptoms.",
        "sensitive": "Consider reducing prolonged outdoor exertion.",
    },
    (101, 150): {
        "level": "Unhealthy for Sensitive Groups",
        "color": "#ff7e00",
        "general": "Reduced tolerance in some people. Active children and adults should limit prolonged outdoor exertion.",
        "sensitive": "People with heart or lung disease, older adults, and children should limit prolonged outdoor exertion.",
    },
    (151, 200): {
        "level": "Unhealthy",
        "color": "#ff0000",
        "general": "Everyone may begin to experience health effects. Limit outdoor activity.",
        "sensitive": "People with heart or lung disease, older adults, and children should avoid all outdoor exertion.",
    },
    (201, 300): {
        "level": "Very Unhealthy",
        "color": "#8f3f97",
        "general": "Health warnings of emergency conditions. Everyone is more likely to be affected.",
        "sensitive": "Remain indoors and keep activity levels low.",
    },
    (301, 500): {
        "level": "Hazardous",
        "color": "#7e0023",
        "general": "Health alert: EMERGENCY CONDITIONS. Everyone is affected.",
        "sensitive": "Everyone should avoid all outdoor exertion. Stay indoors with windows closed.",
    },
}


def get_aqi_info(aqi: int) -> dict:
    for (lo, hi), info in AQI_HEALTH_MAP.items():
        if lo <= aqi <= hi:
            return info
    return AQI_HEALTH_MAP[(301, 500)]


def calculate_health_risk(
    age: int,
    smoker: bool,
    asthma: bool,
    heart_disease: bool,
    outdoor_hours: float,
    current_aqi: int,
    pm25: float = None,
) -> dict:
    """
    Calculate personal pollution risk score (0-100) and personalized advice.
    Returns dict with score, risk_level, multiplier, effects, tips.
    """
    base_score = 0
    multiplier = 1.0
    risk_factors = []

    # ─── Age factor ────────────────────────────────────────────────────────────
    if age < 5:
        age_score = 25
        multiplier *= 2.0
        risk_factors.append("Children under 5 have underdeveloped lungs — **2x more vulnerable**")
    elif age < 12:
        age_score = 20
        multiplier *= 1.7
        risk_factors.append("Children have higher breathing rates — **1.7x more vulnerable**")
    elif age <= 18:
        age_score = 10
        multiplier *= 1.3
        risk_factors.append("Teenagers still developing lungs — **1.3x more vulnerable**")
    elif age <= 35:
        age_score = 5
        risk_factors.append("Healthy adult age group — average risk")
    elif age <= 60:
        age_score = 10
        multiplier *= 1.2
        risk_factors.append("Middle age — slightly elevated risk")
    else:
        age_score = 20
        multiplier *= 1.8
        risk_factors.append("Age 60+ — lungs less efficient — **1.8x more vulnerable**")

    base_score += age_score

    # ─── Smoker ────────────────────────────────────────────────────────────────
    if smoker:
        base_score += 25
        multiplier *= 2.2
        risk_factors.append("Smoking severely damages lung capacity — **2.2x more vulnerable**")

    # ─── Asthma ────────────────────────────────────────────────────────────────
    if asthma:
        base_score += 20
        multiplier *= 1.9
        risk_factors.append("Asthma — airway hypersensitivity to PM2.5 — **1.9x more vulnerable**")

    # ─── Heart disease ─────────────────────────────────────────────────────────
    if heart_disease:
        base_score += 20
        multiplier *= 1.7
        risk_factors.append("Heart disease — PM2.5 enters bloodstream and strains heart — **1.7x more vulnerable**")

    # ─── Outdoor exposure hours ────────────────────────────────────────────────
    if outdoor_hours > 6:
        exposure_score = 25
        risk_factors.append(f"Spending {outdoor_hours}h outdoors — **very high dose exposure**")
    elif outdoor_hours > 3:
        exposure_score = 15
        risk_factors.append(f"Spending {outdoor_hours}h outdoors — moderate exposure")
    elif outdoor_hours > 1:
        exposure_score = 7
        risk_factors.append(f"Spending {outdoor_hours}h outdoors — low exposure")
    else:
        exposure_score = 2
        risk_factors.append("Minimal outdoor time — low exposure")
    base_score += exposure_score

    # ─── AQI adjustment ────────────────────────────────────────────────────────
    if current_aqi > 300:
        aqi_score = 25
    elif current_aqi > 200:
        aqi_score = 20
    elif current_aqi > 150:
        aqi_score = 15
    elif current_aqi > 100:
        aqi_score = 8
    elif current_aqi > 50:
        aqi_score = 3
    else:
        aqi_score = 0
    base_score += aqi_score

    # Final score clipped to 100
    final_score = min(100, int(base_score * min(multiplier, 4.0) / 5.0))

    # ─── Risk level ────────────────────────────────────────────────────────────
    if final_score >= 80:
        risk_level = "CRITICAL"
        risk_color = "#7e0023"
    elif final_score >= 60:
        risk_level = "HIGH"
        risk_color = "#ff0000"
    elif final_score >= 40:
        risk_level = "MODERATE"
        risk_color = "#ff7e00"
    elif final_score >= 20:
        risk_level = "LOW-MODERATE"
        risk_color = "#ffff00"
    else:
        risk_level = "LOW"
        risk_color = "#00e400"

    # ─── Health effects ────────────────────────────────────────────────────────
    aqi_info = get_aqi_info(current_aqi)
    short_term = []
    long_term = []

    if current_aqi > 100:
        short_term.extend(["Throat irritation", "Eye redness", "Sneezing", "Reduced lung function"])
    if current_aqi > 150:
        short_term.extend(["Chest tightness", "Coughing fits", "Shortness of breath on exertion"])
    if current_aqi > 200:
        short_term.extend(["Visible difficulty breathing", "Headache", "Fatigue"])
    if current_aqi > 300:
        short_term.extend(["Respiratory distress", "Nausea", "Dizziness"])

    if outdoor_hours > 2:
        long_term.extend(["Chronic bronchitis risk", "Reduced lung capacity"])
    if outdoor_hours > 4 or smoker:
        long_term.extend(["Increased lung cancer risk", "Cardiovascular stress"])

    # ─── Personalized tips ─────────────────────────────────────────────────────
    tips = []
    if asthma or heart_disease:
        tips.append("🆘 Keep your inhaler/medication **accessible at all times** today")
    if current_aqi > 150:
        tips.append("😷 Wear **N95 mask** — cloth masks block only 30% of PM2.5")
    if outdoor_hours > 2:
        tips.append(f"⏰ Reduce outdoor time from {outdoor_hours}h to **under 1h** today")
    if smoker:
        tips.append("🚭 Do **not smoke indoors** — combined with outdoor pollution, your risk triples")
    if age < 12 or age > 60:
        tips.append("🏠 Stay **fully indoors** — run air purifier or keep windows sealed")
    tips.append("💧 Drink **3+ litres of water** — helps flush pollutants")
    tips.append("🌿 Place **money plant or aloe vera** indoors — natural air purifiers")
    if current_aqi > 200:
        tips.append("🏥 **Visit doctor immediately** if you experience chest pain or breathing difficulty")

    avg_risk_score = 30  # Approximate average healthy adult score
    multiplier_display = round(final_score / max(avg_risk_score, 1), 1)

    return {
        "score": final_score,
        "risk_level": risk_level,
        "risk_color": risk_color,
        "multiplier": multiplier_display,
        "risk_factors": risk_factors,
        "short_term_effects": short_term,
        "long_term_effects": long_term,
        "tips": tips,
        "aqi_level": aqi_info["level"],
        "aqi_color": aqi_info["color"],
    }
