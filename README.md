<div align="center">

# 🌬️ VAYU AI

### *India's First AI-Powered Hyperlocal Pollution Death Risk Predictor*

**"Predicting Where Pollution Will Kill Next — 72 Hours Before It Happens"**

[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red?style=for-the-badge&logo=streamlit)](https://streamlit.io)
[![NVIDIA AI](https://img.shields.io/badge/NVIDIA-Kimi_K2_AI-76b900?style=for-the-badge&logo=nvidia)](https://build.nvidia.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![Zero Cost](https://img.shields.io/badge/Cost-Rs._0-brightgreen?style=for-the-badge)](https://github.com)
[![Hack For Green Bharat](https://img.shields.io/badge/Hack_For_Green_Bharat-2026-orange?style=for-the-badge)](https://github.com)

<img src="https://img.shields.io/badge/Live_APIs-6-blue?style=flat-square" />
<img src="https://img.shields.io/badge/Pages-10-purple?style=flat-square" />
<img src="https://img.shields.io/badge/Lines_of_Code-2200+-green?style=flat-square" />
<img src="https://img.shields.io/badge/Zero_Fake_Data-✓-success?style=flat-square" />

</div>

---

## 🚨 The Problem

> **16 lakh Indians die from air pollution every year** — yet nobody warns them in advance.

- PM2.5 particles are **30× thinner than human hair** — invisible, odourless, lethal
- Hospitals face a **300% surge in respiratory emergencies** during pollution spikes with zero advance notice
- Rural citizens, children, and the elderly are the most vulnerable — and the least informed
- **No existing system predicts** dangerous air quality 48–72 hours ahead at a hyperlocal level

**VAYU AI solves this.** It monitors live pollution sensors, combines real weather forecasts with AI analysis, and sends life-saving predictions 72 hours before danger strikes.

---

## ✅ Solution — What VAYU AI Does

| Feature | Description | Data Source |
|---|---|---|
| 🏠 **Live AQI Dashboard** | Real-time PM2.5, PM10, NO₂, CO + pollutant breakdown vs WHO limits | OpenAQ + WAQI |
| 📈 **72-Hour AQI Forecast** | Real 120h PM2.5 forecast blended with live sensor reading | Open-Meteo Air Quality API |
| 🗺️ **Pollution Heatmap** | Interactive map of all Indian cities + NASA satellite fire alerts | Folium + NASA FIRMS |
| 🏥 **Health Risk Calculator** | Personal risk score 0–100 based on age, conditions, live AQI | WHO exposure-response models |
| 🏙️ **Multi-City Comparison** | Side-by-side live AQI comparison for up to 5 cities | OpenAQ + WAQI |
| 🚑 **Hospital Alert System** | Predicts extra beds, medicines, staff needed 72h ahead | Derived from AQI forecast |
| 📊 **Historical Analysis** | 30-day pollution trends from real weather archive | Open-Meteo Archive API |
| 🌱 **Green Action Tracker** | Log eco-actions, earn points, track CO₂ saved | Scientific emission constants |
| 💨 **Carbon Calculator** | Personal footprint using published emission factors | IPCC + India Grid data |
| 🤖 **AI Chatbot** | Real-time conversational AI with live AQI context | NVIDIA Kimi K2 (zero fallbacks) |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        VAYU AI v3.0                             │
│            India's Pollution Death Risk Predictor               │
└─────────────────────────────────────────────────────────────────┘

                         ┌─────────────┐
                         │    User     │
                         │  (Browser)  │
                         └──────┬──────┘
                                │ HTTP
                         ┌──────▼──────┐
                         │   app.py    │
                         │  Streamlit  │
                         │  10 Pages   │
                         │ Dark+Light  │
                         └──────┬──────┘
                                │
          ┌─────────────────────┼──────────────────────┐
          │                     │                      │
   ┌──────▼──────┐      ┌──────▼──────┐      ┌────────▼───────┐
   │data_fetcher │      │predictor.py │      │gemini_explainer│
   │    .py      │      │             │      │      .py       │
   │ All API I/O │      │ 72h Forecast│      │ NVIDIA Kimi K2 │
   └──────┬──────┘      └──────┬──────┘      └────────┬───────┘
          │                     │                      │
   ┌──────▼──────┐       ┌──────▼─────┐               │
   │health_calc  │       │hospital_   │               │
   │carbon_calc  │       │predictor   │               │
   │   utils     │       │  utils     │               │
   └─────────────┘       └────────────┘               │
                                                        │
─────────────────── EXTERNAL APIs ───────────────────────
                                                        │
  ┌──────────┐  ┌──────────┐  ┌───────────┐  ┌────────┴──────┐
  │  OpenAQ  │  │   WAQI   │  │Open-Meteo │  │  NVIDIA API   │
  │  (free)  │  │ (geo+city│  │Forecast + │  │  Kimi K2 AI   │
  │  PM2.5   │  │  demo)   │  │  Archive  │  │  Real-time    │
  └──────────┘  └──────────┘  └───────────┘  └───────────────┘
                    ┌──────────────┐  ┌────────────────┐
                    │  NASA FIRMS  │  │   Nominatim    │
                    │  Satellite   │  │ OpenStreetMap  │
                    │  Fire Data   │  │  Geocoding     │
                    └──────────────┘  └────────────────┘
```

---

## 📁 Project Structure

```
vayu-ai/
├── 📄 app.py                   # Main Streamlit app — 10 pages, dark/light theme (760 lines)
├── ⚙️  config.py               # API keys, AQI levels (EPA), WHO limits, emission factors
├── 🔌 data_fetcher.py          # All API calls — WAQI geo+city, OpenAQ, Open-Meteo, NASA FIRMS
├── 🧠 predictor.py             # 72h AQI forecast via Open-Meteo Air Quality API
├── 🤖 gemini_explainer.py      # NVIDIA Kimi K2 AI integration — zero predefined responses
├── 💊 health_calculator.py     # Personal health risk scoring engine (WHO models)
├── 🏥 hospital_predictor.py    # Hospital load prediction from AQI forecast
├── 🌱 carbon_calculator.py     # Carbon footprint (IPCC + India Grid emission factors)
├── 💬 chatbot.py               # Chat session state management
├── 🛠️  utils.py                # AQI colors, labels, WHO exceedance, formatters
├── 📋 requirements.txt         # All Python dependencies
├── 📖 README.md                # This file
└── .streamlit/
    ├── config.toml             # Dark theme defaults
    └── secrets.toml            # API keys (not committed)
```

---

## 🔌 APIs & Data Sources

| Service | Purpose | Cost | Auth |
|---|---|---|---|
| [OpenAQ v2](https://api.openaq.org) | Live PM2.5, PM10, NO₂, CO sensor data | Free | None |
| [WAQI](https://aqicn.org/api/) | Backup AQI via city name + geo-coordinates | Free | Demo token |
| [Open-Meteo](https://open-meteo.com) | 120h weather + PM2.5 forecast | Free | None |
| [Open-Meteo Archive](https://archive-api.open-meteo.com) | 30-day historical weather | Free | None |
| [NASA FIRMS](https://firms.modaps.eosdis.nasa.gov) | Satellite wildfire detection | Free | API key |
| [Nominatim OSM](https://nominatim.openstreetmap.org) | City → lat/lon geocoding | Free | None |
| [NVIDIA Kimi K2](https://build.nvidia.com) | Real-time conversational AI chatbot | Free tier | API key |

**Total monthly API cost: Rs. 0**

---

## 🧪 Zero Fake Data Policy

VAYU AI enforces a **strict no-simulated-data architecture**. Every number displayed comes from a real API, a scientific constant, or user input. Nothing is fabricated.

| Module | Data Source | Fallback on Failure |
|---|---|---|
| Live AQI | OpenAQ → WAQI geo → WAQI city | Returns `None`, shows error card |
| 72h Forecast | Open-Meteo Air Quality API | Returns `None`, hides chart |
| AI Chatbot | NVIDIA Kimi K2 (live API call) | Returns plain error message |
| Health Risk | WHO exposure-response formula | Pure math, no API needed |
| Carbon Footprint | IPCC/India Grid emission factors | Scientific constants |
| Hospital Load | Formula on real AQI forecast | Returns `None` if no forecast |
| Historical | Open-Meteo Archive (real data) | Error message |

```python
# Example: data_fetcher.py — returns None, never invents data
def get_best_aqi_data(city, lat, lon, ...):
    r = get_waqi_geo_data(lat, lon)   # Try 1: WAQI geo-coordinates
    if r: return r
    r = get_waqi_data(city)            # Try 2: WAQI by city name
    if r: return r
    r = get_openaq_data(city)          # Try 3: OpenAQ
    if r: return r
    return None                        # Never return fake data
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Nytrynox/vayu-ai.git
cd vayu-ai

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add API keys (optional — app works with defaults)
# Edit .streamlit/secrets.toml

# 4. Run the app
streamlit run app.py
```

App opens at **http://localhost:8501**

### API Keys (Optional)
The app works out-of-the-box with free/demo API tokens. To use your own:

```toml
# .streamlit/secrets.toml
NVIDIA_API_KEY = "nvapi-..."      # https://build.nvidia.com (free tier)
NASA_FIRMS_KEY = "..."            # https://firms.modaps.eosdis.nasa.gov/api/
WAQI_TOKEN = "..."                # https://aqicn.org/api/ (free)
```

---

## ☁️ Deployment

### Streamlit Community Cloud (Recommended — Free)
1. Fork this repo to your GitHub account
2. Go to **[share.streamlit.io](https://share.streamlit.io)**
3. Click **New App** → select this repo → `app.py`
4. In **Advanced settings → Secrets**, paste your API keys
5. Click **Deploy** → live in ~60 seconds

### Self-Hosted
```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

---

## 📊 Technical Details

### 72-Hour Forecast Engine
```
Open-Meteo Air Quality API
        ↓
  120h PM2.5 hourly forecast
        ↓
  Blend with live sensor (0–6h)
  [weight = (6-i)/6 × live + i/6 × forecast]
        ↓
  Apply NASA fire proximity scaling
  [multiplier = 1 + (100-km)/200 if fire < 100km]
        ↓
  PM2.5 → AQI via CPCB breakpoints
        ↓
  72h time-series with peak marker
```

### Health Risk Model
```
risk = base_aqi_score
     × age_factor           (1.0 → 3.0 based on age)
     × smoker_factor         (2.0x if smoker)
     × asthma_factor         (3.0x if asthmatic)
     × heart_factor          (2.5x if heart condition)
     × outdoor_exposure      (hours/12)
→ Normalized 0–100
→ Mapped to: Safe / Moderate / High / Emergency
```

### Data Priority Chain
```
WAQI Geo-Coordinates (most reliable, any location)
    ↓ if None
WAQI City Name (good for major Indian cities)
    ↓ if None  
OpenAQ v2 (covers CPCB-connected stations)
    ↓ if None
Return None → UI shows "No data available"
```

---

## 🎯 Impact

| Stakeholder | Impact |
|---|---|
| 🧑 **Citizens** | 72h advance warnings — know when to stay indoors, which mask to buy |
| 🏥 **Hospitals** | Prepare extra beds and stock medicines 3 days before surge |
| 🏛️ **Government** | Data-driven smog response plans with hyperlocal granularity |
| 🏫 **Schools** | Decide closures based on real forecasts, not guesswork |
| 💰 **Economy** | Prevent Rs. 2.5 lakh crore annual health cost from air pollution |

---

## 🛣️ Roadmap

- [ ] SMS/WhatsApp alerts for rural areas without internet
- [ ] Ward-level predictions using satellite imagery (Sentinel-5P)
- [ ] Integration with CPCB real-time monitoring network
- [ ] Flutter mobile app with push notifications
- [ ] Multi-language: Hindi, Tamil, Telugu, Bengali, Marathi
- [ ] B2G licensing to state pollution control boards
- [ ] Hospital management system API integration

---

## 🧰 Tech Stack

```
Language:      Python 3.11
Framework:     Streamlit 1.28+
AI:            NVIDIA Kimi K2 (moonshotai/kimi-k2-instruct-0905)
Visualization: Plotly 5.x + Folium
Data:          Pandas + NumPy
Requests:      requests (all API calls, timeout=12s)
PDF:           fpdf2
```

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

<div align="center">

**Built for Hack For Green Bharat 2026**

*16 lakh Indians die from air pollution yearly. VAYU warns them 72 hours ahead.*

[![Deploy on Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

</div>
