"""
utils.py — VAYU AI
Helper functions used across modules.
"""

from config import AQI_LEVELS, WHO_LIMITS


def get_aqi_color(aqi: int) -> str:
    """Return color hex for an AQI value."""
    if aqi is None:
        return "#64748b"
    try:
        aqi = int(aqi)
    except (TypeError, ValueError):
        return "#64748b"
    if aqi <= 50: return "#22c55e"
    if aqi <= 100: return "#eab308"
    if aqi <= 150: return "#f97316"
    if aqi <= 200: return "#ef4444"
    if aqi <= 300: return "#7c3aed"
    return "#1f2937"


def get_aqi_label(aqi: int) -> str:
    """Return human-readable label for an AQI value."""
    if aqi is None:
        return "Unknown"
    try:
        aqi = int(aqi)
    except (TypeError, ValueError):
        return "Unknown"
    if aqi <= 50: return "Good"
    if aqi <= 100: return "Moderate"
    if aqi <= 150: return "Unhealthy (Sensitive)"
    if aqi <= 200: return "Unhealthy"
    if aqi <= 300: return "Very Unhealthy"
    return "Hazardous"


def get_aqi_message(aqi: int) -> str:
    """Return health guidance for an AQI value."""
    for level_name, info in AQI_LEVELS.items():
        lo, hi = info["range"]
        if lo <= (aqi or 0) <= hi:
            return info["message"]
    return "Extreme danger. Stay indoors. Seek medical help if breathing is difficult."


def get_who_exceedance(pollutant: str, value: float) -> dict:
    """Check how much a value exceeds WHO safe limits."""
    if value is None or pollutant not in WHO_LIMITS:
        return {"exceeds": False, "ratio": 0, "message": "N/A"}
    limit = WHO_LIMITS[pollutant]["limit"]
    ratio = round(value / limit, 1)
    return {
        "exceeds": value > limit,
        "ratio": ratio,
        "message": f"{ratio}x WHO limit" if value > limit else "Within safe limits",
    }


def format_number(n, decimals=1) -> str:
    """Format large numbers for display."""
    if n is None:
        return "N/A"
    if n >= 10_000_000:
        return f"{n / 10_000_000:.{decimals}f} Cr"
    if n >= 100_000:
        return f"{n / 100_000:.{decimals}f} L"
    if n >= 1000:
        return f"{n / 1000:.{decimals}f}K"
    return str(round(n, decimals))
