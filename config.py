"""
config.py — VAYU AI
Central configuration. NO FAKE/SAMPLE DATA.
All data comes from live APIs or user input only.
"""

# ─── API Keys (user provides via sidebar or st.secrets) ────────────────────────
NVIDIA_API_KEY = "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"
NVIDIA_MODEL = "moonshotai/kimi-k2-instruct-0905"
NVIDIA_API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"

NASA_FIRMS_KEY = "c347b18f13d1c90937feb32ecfd09a21"
WAQI_TOKEN = "demo"

# ─── AQI Levels (US EPA Standard — scientific reference, not fake data) ────────
AQI_LEVELS = {
    "Good":        {"range": (0, 50),    "color": "#22c55e", "emoji": "✅", "message": "Air quality is satisfactory. Safe for all activities."},
    "Moderate":    {"range": (51, 100),   "color": "#eab308", "emoji": "⚠️", "message": "Acceptable. Sensitive individuals should limit prolonged outdoor exertion."},
    "USG":         {"range": (101, 150),  "color": "#f97316", "emoji": "🟠", "message": "Unhealthy for sensitive groups. Children, elderly, and asthma patients should limit outdoor activity."},
    "Unhealthy":   {"range": (151, 200),  "color": "#ef4444", "emoji": "🔴", "message": "Everyone may begin to experience health effects. Limit outdoor exertion."},
    "Very Unhealthy": {"range": (201, 300), "color": "#7c3aed", "emoji": "🟣", "message": "Health alert. Everyone should avoid prolonged outdoor exertion."},
    "Hazardous":   {"range": (301, 500),  "color": "#1f2937", "emoji": "⚫", "message": "Emergency conditions. Everyone should avoid ALL outdoor activity."},
}

# ─── WHO Safe Limits (scientific constants, not fake data) ─────────────────────
WHO_LIMITS = {
    "pm25": {"limit": 15, "unit": "µg/m³", "name": "PM2.5"},
    "pm10": {"limit": 45, "unit": "µg/m³", "name": "PM10"},
    "no2":  {"limit": 25, "unit": "µg/m³", "name": "NO₂"},
    "co":   {"limit": 4,  "unit": "mg/m³",  "name": "CO"},
}

# ─── India CPCB AQI Breakpoints (official government standard) ─────────────────
CPCB_PM25_BREAKPOINTS = [
    (0, 30, 0, 50),        # Good
    (31, 60, 51, 100),     # Satisfactory
    (61, 90, 101, 200),    # Moderate
    (91, 120, 201, 300),   # Poor
    (121, 250, 301, 400),  # Very Poor
    (250, 500, 401, 500),  # Severe
]

# ─── Carbon Emission Factors (published scientific data) ───────────────────────
EMISSION_FACTORS = {
    "car_per_km": 0.21,         # kg CO2/km (average Indian car)
    "bike_per_km": 0.05,        # kg CO2/km (2-wheeler)
    "auto_per_km": 0.08,        # kg CO2/km (auto-rickshaw)
    "bus_per_km": 0.03,         # kg CO2/km per passenger
    "metro_per_km": 0.01,       # kg CO2/km per passenger
    "flight_per_trip": 250.0,   # kg CO2 per domestic one-way flight
    "ac_per_hour": 1.5,         # kg CO2/hour
    "electricity_per_unit": 0.82,  # kg CO2/kWh (India grid average)
    "lpg_per_cylinder": 42.5,   # kg CO2 per 14.2kg cylinder
    "veg_diet_daily": 2.5,      # kg CO2/day
    "nonveg_diet_daily": 5.0,   # kg CO2/day
}

INDIA_AVERAGE_ANNUAL_CARBON = 1.9  # tonnes CO2 per capita
WORLD_AVERAGE_ANNUAL_CARBON = 4.7  # tonnes CO2 per capita

# ─── App Settings ─────────────────────────────────────────────────────────────
APP_NAME = "VAYU AI"
APP_TAGLINE = "Predicting Where Pollution Will Kill Next — 72 Hours Before It Happens"
APP_VERSION = "3.0"
TIMEOUT = 12  # API timeout in seconds
