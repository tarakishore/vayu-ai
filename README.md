# 🌫️ VAYU AI
### India's First AI-Powered Hyperlocal Pollution Death Risk Predictor

Every year **16 lakh Indians die from air pollution**. But nobody warns them 48 hours before danger strikes.

**VAYU AI changes that.**

---

## What It Does

- 🔴 **Live AQI Dashboard** — Real PM2.5, PM10, NO2, CO for any Indian city
- 📈 **72-Hour AQI Prediction** — Real 120-hour forecast data from Open-Meteo Air Quality
- 🗺️ **Hyperlocal Pollution Heatmap** — Interactive Folium map with sensor data
- 🛰️ **NASA Stubble Fire Detection** — Satellite fire alerts within 300km
- 🫁 **Personal Health Risk Calculator** — Your custom danger score 0–100
- 🏙️ **Multi-City Comparison** — Compare up to 5 cities side by side
- 🏥 **Hospital Preparedness Predictor** — Extra beds & medicines to stock
- 📊 **Historical Trend Analysis** — Last 30 days pollution patterns
- 🌿 **Green Action Tracker** — Earn points for eco-friendly actions
- 🤖 **VAYU AI Chatbot** — Powered by NVIDIA Kimi K2 AI

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Python + Streamlit |
| AI/NLP | NVIDIA Kimi K2 AI |
| Forecast | Open-Meteo Air Quality API |
| Visualization | Plotly + Folium |
| Live AQI | OpenAQ v2 API + WAQI |
| Weather | Open-Meteo (free, no key) |
| Fire Data | NASA FIRMS (free key) |
| Geocoding | Nominatim OpenStreetMap |

---

## Setup

**1. Clone and install:**
```bash
git clone https://github.com/yourname/vayu-ai.git
cd vayu-ai
pip install -r requirements.txt
```

**2. Run:**
```bash
streamlit run app.py
```

**3. (Optional) Add API keys in the app:**
- NVIDIA API Key → [build.nvidia.com](https://build.nvidia.com)
- NASA FIRMS Key → [firms.modaps.eosdis.nasa.gov](https://firms.modaps.eosdis.nasa.gov/api/area/) 
- WAQI Token → [aqicn.org/api](https://aqicn.org/api/) 

> 💡 **Zero Fake Data Policy**: VAYU AI enforces a strict no-simulated-data architecture. It requires internet connectivity to fetch live readings.

---

## Free APIs Used

| API | Purpose | Key Required |
|---|---|---|
| OpenAQ v2 | Live pollution readings | No |
| Open-Meteo | 72h weather & AQI forecast | No |
| Nominatim OSM | City geocoding | No |
| Open-Meteo Archive | 30-day history | No |
| NASA FIRMS | Satellite fire data | Free key |
| WAQI | Backup AQI data | Free key |
| NVIDIA Kimi | AI chatbot | Free key |

---

## Folder Structure

```
vayu-ai/
├── app.py                  ← Main Streamlit app (all 10 features)
├── data_fetcher.py         ← All API calls
├── predictor.py            ← Open-Meteo Air Quality Forecast integration
├── gemini_explainer.py     ← NVIDIA Kimi AI integration
├── health_calculator.py    ← Personal health risk
├── carbon_calculator.py    ← Carbon footprint
├── hospital_predictor.py   ← Hospital bed prediction
├── chatbot.py              ← Chat session management
├── requirements.txt
└── README.md
```

---

## Deploy Free on Streamlit Cloud

1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect GitHub → select repo → Click Deploy
4. Add API keys in Streamlit Secrets

---

**Built for:** Hack For Green Bharat Hackathon 2026 🇮🇳
