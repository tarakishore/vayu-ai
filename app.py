"""
VAYU AI — India's First AI-Powered Hyperlocal Pollution Death Risk Predictor
Premium Design · Dark + Light Theme · Location Search · NO FAKE DATA · All 10 Pages
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="VAYU AI", page_icon="🌬️", layout="wide", initial_sidebar_state="expanded")

# ─── State ─────────────────────────────────────────────────────────────────────
defaults = {
    "city": "", "lat": None, "lon": None, "aqi_data": None, "weather": None,
    "fires": None, "prediction": None, "green_points": 0, "green_log": [],
    "multi_cities": [], "auto_located": False, "data_fetched": False,
    "theme": "Dark", "vayu_chat_history": [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─── THEME ─────────────────────────────────────────────────────────────────────
THEMES = {
    "Dark": {
        "bg": "#0b0f19", "bg2": "#111827", "bg3": "#1a1f2e",
        "surface": "rgba(255,255,255,0.03)", "surface_border": "rgba(255,255,255,0.06)",
        "surface_hover": "rgba(255,255,255,0.06)",
        "text": "#e2e8f0", "text2": "#94a3b8", "text3": "#64748b",
        "accent": "#3b82f6", "accent2": "#60a5fa", "accent_bg": "rgba(59,130,246,0.08)",
        "red": "#ef4444", "orange": "#f97316", "yellow": "#eab308", "green": "#22c55e",
        "sidebar_bg": "linear-gradient(180deg,#0f1629 0%,#111827 100%)",
        "hero_bg": "linear-gradient(135deg,#0f172a 0%,#1e293b 50%,#0f172a 100%)",
        "input_bg": "#1e293b", "input_border": "#334155",
        "plotly": "plotly_dark", "plot_bg": "rgba(15,20,30,0.5)",
        "map_tiles": "CartoDB dark_matter",
        "danger_bg": "rgba(239,68,68,0.06)", "danger_text": "#fca5a5",
        "warn_bg": "rgba(251,146,60,0.06)", "warn_text": "#fed7aa",
        "safe_bg": "rgba(34,197,94,0.06)", "safe_text": "#86efac",
        "info_bg": "rgba(59,130,246,0.06)", "info_text": "#93c5fd",
    },
    "Light": {
        "bg": "#f1f5f9", "bg2": "#ffffff", "bg3": "#e2e8f0",
        "surface": "rgba(255,255,255,0.9)", "surface_border": "rgba(0,0,0,0.06)",
        "surface_hover": "rgba(0,0,0,0.03)",
        "text": "#0f172a", "text2": "#475569", "text3": "#94a3b8",
        "accent": "#2563eb", "accent2": "#3b82f6", "accent_bg": "rgba(37,99,235,0.06)",
        "red": "#dc2626", "orange": "#ea580c", "yellow": "#ca8a04", "green": "#16a34a",
        "sidebar_bg": "linear-gradient(180deg,#ffffff 0%,#f8fafc 100%)",
        "hero_bg": "linear-gradient(135deg,#1e293b 0%,#334155 50%,#1e293b 100%)",
        "input_bg": "#ffffff", "input_border": "#cbd5e1",
        "plotly": "plotly_white", "plot_bg": "rgba(255,255,255,0.6)",
        "map_tiles": "CartoDB positron",
        "danger_bg": "rgba(220,38,38,0.06)", "danger_text": "#b91c1c",
        "warn_bg": "rgba(234,88,12,0.06)", "warn_text": "#c2410c",
        "safe_bg": "rgba(22,163,74,0.06)", "safe_text": "#15803d",
        "info_bg": "rgba(37,99,235,0.06)", "info_text": "#1d4ed8",
    },
}
T = THEMES[st.session_state.theme]

# ─── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(f"""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
*{{font-family:'Inter',sans-serif;}}
@keyframes fadeUp{{from{{opacity:0;transform:translateY(12px)}}to{{opacity:1;transform:translateY(0)}}}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:0.5}}}}
@keyframes shimmer{{0%{{background-position:-600px 0}}100%{{background-position:600px 0}}}}

.stApp{{background:{T['bg']} !important;color:{T['text']} !important;}}
header[data-testid="stHeader"]{{background:transparent !important;}}
footer{{visibility:hidden;}}
[data-testid="stSidebar"]{{background:{T['bg2']} !important;border-right:1px solid {T['surface_border']} !important;}}
[data-testid="stSidebar"] p,[data-testid="stSidebar"] label,[data-testid="stSidebar"] div,[data-testid="stSidebar"] span{{color:{T['text']} !important;}}
.stMarkdown p,.stMarkdown li,.stMarkdown span{{color:{T['text']};}}

/* Cards */
.card{{background:{T['surface']};border:1px solid {T['surface_border']};border-radius:16px;
  padding:24px;animation:fadeUp 0.4s ease-out;transition:all 0.3s;}}
.card:hover{{border-color:{T['accent']};box-shadow:0 0 0 1px {T['accent']};}}

/* Hero */
.hero{{background:{T['hero_bg']};border-radius:20px;padding:36px 40px;margin-bottom:28px;
  position:relative;overflow:hidden;border:1px solid rgba(255,255,255,0.05);}}
.hero h1{{font-size:2.2rem;font-weight:900;color:#fff;margin:0;letter-spacing:-1px;}}
.hero .sub{{color:rgba(255,255,255,0.5);font-size:0.85rem;margin-top:8px;}}
.hero .badge{{display:inline-block;background:rgba(59,130,246,0.2);color:#93c5fd;padding:4px 14px;
  border-radius:20px;font-size:0.72rem;font-weight:600;margin-top:12px;letter-spacing:0.5px;}}

/* Big number display */
.bignum{{text-align:center;padding:28px;}}
.bignum .value{{font-size:4rem;font-weight:900;line-height:1;letter-spacing:-3px;}}
.bignum .label{{font-size:0.85rem;color:{T['text3']};margin-top:8px;font-weight:500;}}
.bignum .meta{{font-size:0.72rem;color:{T['text3']};margin-top:4px;}}

/* Stat card */
.stat{{background:{T['surface']};border:1px solid {T['surface_border']};border-radius:14px;
  padding:18px 22px;text-align:center;animation:fadeUp 0.4s ease-out;transition:all 0.2s;}}
.stat:hover{{transform:translateY(-2px);border-color:{T['accent']};}}
.stat .v{{font-size:1.6rem;font-weight:800;line-height:1.1;}}
.stat .l{{font-size:0.72rem;color:{T['text3']};margin-top:4px;font-weight:500;text-transform:uppercase;letter-spacing:0.5px;}}

/* Section header */
.sh{{font-size:1.05rem;font-weight:700;color:{T['text']};margin:28px 0 16px;display:flex;align-items:center;gap:10px;}}
.sh::before{{content:'';width:4px;height:20px;border-radius:2px;background:{T['accent']};display:inline-block;}}

/* Alerts */
.al{{border-radius:12px;padding:14px 18px;margin:10px 0;border-left:4px solid;font-size:0.88rem;animation:fadeUp 0.3s ease-out;}}
.al-d{{background:{T['danger_bg']};border-color:{T['red']};color:{T['danger_text']};}}
.al-w{{background:{T['warn_bg']};border-color:{T['orange']};color:{T['warn_text']};}}
.al-s{{background:{T['safe_bg']};border-color:{T['green']};color:{T['safe_text']};}}
.al-i{{background:{T['info_bg']};border-color:{T['accent']};color:{T['info_text']};}}

/* Tips */
.tip{{background:{T['surface']};border:1px solid {T['surface_border']};border-radius:12px;
  padding:12px 16px;margin:6px 0;font-size:0.85rem;color:{T['text2']};transition:all 0.2s;}}
.tip:hover{{background:{T['surface_hover']};transform:translateX(3px);border-color:{T['accent']};}}

/* Progress bar */
.pbar{{background:{T['bg3']};border-radius:6px;height:8px;overflow:hidden;margin-top:6px;}}
.pfill{{height:100%;border-radius:6px;background:linear-gradient(90deg,var(--c1),var(--c2));
  position:relative;transition:width 1s ease;}}

/* Footer */
.foot{{text-align:center;padding:20px 0;margin-top:40px;border-top:1px solid {T['surface_border']};
  color:{T['text3']};font-size:0.72rem;}}

/* Inputs & controls */
[data-testid="stMetricValue"]{{color:{T['text']} !important;font-weight:800 !important;}}
[data-testid="stMetricLabel"]{{color:{T['text3']} !important;}}
.stTextInput input,.stNumberInput input{{background:{T['input_bg']} !important;color:{T['text']} !important;border-color:{T['input_border']} !important;}}
.stRadio label p,.stCheckbox label p{{color:{T['text2']} !important;}}
.stSlider .stMarkdown p{{color:{T['text3']} !important;}}
</style>""", unsafe_allow_html=True)

# ─── Imports ───────────────────────────────────────────────────────────────────
import data_fetcher as df_mod
import predictor as pred_mod
import health_calculator as hc
import carbon_calculator as cc
import hospital_predictor as hp
import chatbot as cb

NASA_KEY = "c347b18f13d1c90937feb32ecfd09a21"
WAQI_TOKEN = "demo"
try:
    NASA_KEY = st.secrets.get("NASA_FIRMS_KEY", NASA_KEY)
    WAQI_TOKEN = st.secrets.get("WAQI_TOKEN", WAQI_TOKEN)
except Exception:
    pass

# ─── Auto-locate ───────────────────────────────────────────────────────────────
if not st.session_state.auto_located:
    loc = df_mod.get_user_location()
    if loc:
        st.session_state.city = loc["city"]
        st.session_state.lat = loc["lat"]
        st.session_state.lon = loc["lon"]
    else:
        st.session_state.city = "Delhi"
        st.session_state.lat, st.session_state.lon = 28.6139, 77.2090
    st.session_state.auto_located = True

def fetch_city_data():
    city, lat, lon = st.session_state.city, st.session_state.lat, st.session_state.lon
    if not lat:
        return
    st.session_state.aqi_data = df_mod.get_best_aqi_data(city, lat, lon, WAQI_TOKEN)
    st.session_state.weather = df_mod.get_weather_forecast(lat, lon)
    st.session_state.fires = df_mod.get_nasa_fires(lat, lon, days=2, api_key=NASA_KEY)
    fd = 300.0
    f = st.session_state.fires
    if f is not None and not f.empty and "distance_km" in f.columns:
        fd = float(f["distance_km"].min())
    ad = st.session_state.aqi_data
    if ad and ad.get("pm25") is not None:
        p = pred_mod.get_predictor()
        st.session_state.prediction = p.predict_72h(
            current_pm25=ad["pm25"], weather_forecast=st.session_state.weather, fire_distance_km=fd)
    st.session_state.data_fetched = True

if not st.session_state.data_fetched:
    fetch_city_data()

# ─── Helpers ───────────────────────────────────────────────────────────────────
def aqc(aqi):
    try: aqi = int(aqi)
    except Exception: return T['text3']
    if aqi <= 50: return T['green']
    if aqi <= 100: return T['yellow']
    if aqi <= 150: return T['orange']
    if aqi <= 200: return T['red']
    return "#7c3aed"

def aql(aqi):
    try: aqi = int(aqi)
    except Exception: return "Unknown"
    if aqi <= 50: return "Good"
    if aqi <= 100: return "Moderate"
    if aqi <= 150: return "Unhealthy (Sensitive)"
    if aqi <= 200: return "Unhealthy"
    if aqi <= 300: return "Very Unhealthy"
    return "Hazardous"

PL = dict(template=T["plotly"], paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor=T["plot_bg"],
          font=dict(family="Inter", color=T["text"]), margin=dict(l=20,r=20,t=40,b=20))

def nodata(m):
    st.markdown(f'<div class="al al-w"><strong>No Data</strong> — {m}</div>', unsafe_allow_html=True)

# ─── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""<div style="padding:8px 0">
        <div style="font-size:1.6rem;font-weight:900;color:{T['text']};letter-spacing:-1px">
            VAYU <span style="color:{T['accent']}">AI</span>
        </div>
        <div style="font-size:0.72rem;color:{T['text3']};margin-top:2px;letter-spacing:0.3px">
            POLLUTION DEATH RISK PREDICTOR
        </div>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")

    # Theme toggle
    st.markdown(f'<div style="font-size:0.72rem;font-weight:600;color:{T["text3"]};letter-spacing:0.5px;margin-bottom:4px">THEME</div>', unsafe_allow_html=True)
    new_theme = st.radio("Theme", ["Dark", "Light"], index=0 if st.session_state.theme == "Dark" else 1, horizontal=True, label_visibility="collapsed")
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.rerun()
    st.markdown("---")

    page = st.radio("Navigate", [
        "Home Dashboard", "72H Prediction", "Pollution Heatmap", "Health Risk",
        "City Comparison", "Hospital Alert", "Historical Trends", "Green Tracker",
        "Carbon Calculator", "AI Chatbot",
    ], label_visibility="collapsed")
    st.markdown("---")

    # Location search
    st.markdown(f'<div style="font-size:0.72rem;font-weight:600;color:{T["text3"]};letter-spacing:0.5px;margin-bottom:4px">LOCATION</div>', unsafe_allow_html=True)
    sq = st.text_input("Search", placeholder="Type a city name...", label_visibility="collapsed")
    if sq and len(sq) >= 2:
        results = df_mod.search_locations(sq)
        if results:
            for r in results[:5]:
                if st.button(f"{r['name']}", key=f"loc_{r['lat']}_{r['lon']}", use_container_width=True):
                    st.session_state.city = r["name"].split(",")[0].strip()
                    st.session_state.lat = r["lat"]
                    st.session_state.lon = r["lon"]
                    st.session_state.data_fetched = False
                    st.session_state.prediction = None
                    st.session_state.aqi_data = None
                    st.rerun()

    st.markdown(f"""<div style="margin-top:16px;padding:12px;background:{T['surface']};border:1px solid {T['surface_border']};border-radius:10px">
        <div style="font-size:0.78rem;font-weight:600;color:{T['text']}">{st.session_state.city or 'Unknown'}</div>
        <div style="font-size:0.68rem;color:{T['text3']}">Auto-detected · Search above to change</div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f'<div style="text-align:center;color:{T["text3"]};font-size:0.68rem;margin-top:20px;font-weight:500">Hack For Green Bharat 2026</div>', unsafe_allow_html=True)

# ─── Hero ──────────────────────────────────────────────────────────────────────
now = datetime.now()
st.markdown(f"""<div class="hero">
    <div class="badge">LIVE DATA · {st.session_state.city.upper()}</div>
    <h1>VAYU <span style="color:{T['accent']}">AI</span></h1>
    <div class="sub">India's First AI-Powered Hyperlocal Pollution Death Risk Predictor · {now.strftime("%A, %d %B %Y | %I:%M %p IST")}</div>
</div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — HOME
# ═══════════════════════════════════════════════════════════════════════════════
if page == "Home Dashboard":
    ad = st.session_state.aqi_data
    city = st.session_state.city
    if ad is None:
        nodata("Could not fetch AQI from APIs (OpenAQ / WAQI). Try a different city or check your internet connection.")
    else:
        aqi = ad.get("aqi")
        pm25 = ad.get("pm25")
        pm10 = ad.get("pm10")
        no2 = ad.get("no2")
        co = ad.get("co")

        if aqi is None:
            nodata("AQI value not available from the API for this location.")
        else:
            color = aqc(aqi)
            label = aql(aqi)

            c1, c2 = st.columns([1, 2])
            with c1:
                st.markdown(f"""<div class="card" style="border-top:3px solid {color}">
                    <div class="bignum">
                        <div style="font-size:0.78rem;color:{T['text3']}">Current AQI — {city}</div>
                        <div class="value" style="color:{color}">{aqi}</div>
                        <div class="label" style="color:{color};font-weight:700;font-size:0.95rem">{label}</div>
                        <div class="meta">Source: {ad.get('source','')} · {ad.get('timestamp','')[:16]}</div>
                    </div>
                </div>""", unsafe_allow_html=True)

            with c2:
                st.markdown('<div class="sh">Pollutant Breakdown vs WHO Limits</div>', unsafe_allow_html=True)
                for name, (val, lim) in {"PM2.5": (pm25, 15), "PM10": (pm10, 45), "NO2": (no2, 25), "CO mg/m³": (co, 4)}.items():
                    if val is None:
                        continue
                    pct = min(100, int((val / max(lim * 3, 1)) * 100))
                    bc = T['red'] if val > lim else T['green']
                    bl = "#fca5a5" if val > lim else "#86efac"
                    ex = f"{round(val / lim, 1)}x WHO" if val > lim else "Safe"
                    st.markdown(f"""<div style="margin-bottom:14px;animation:fadeUp 0.4s">
                        <div style="display:flex;justify-content:space-between;font-size:0.82rem;color:{T['text2']}">
                            <span>{name}</span>
                            <span style="color:{bc};font-weight:700">{val} µg/m³ — {ex}</span>
                        </div>
                        <div class="pbar"><div class="pfill" style="width:{pct}%;--c1:{bc};--c2:{bl}"></div></div>
                        <div style="font-size:0.68rem;color:{T['text3']};margin-top:2px">WHO limit: {lim}</div>
                    </div>""", unsafe_allow_html=True)

            pred = st.session_state.prediction
            if pred:
                st.markdown("---")
                st.markdown('<div class="sh">72-Hour Forecast Snapshot</div>', unsafe_allow_html=True)
                sh = sum(1 for a in pred["aqi"] if a <= 100)
                dh = sum(1 for a in pred["aqi"] if a > 200)
                for col_item, val, lbl, vc in zip(
                    st.columns(4),
                    [str(pred["peak_aqi"]), pred["peak_time"][11:16], f"{sh}/72", str(dh)],
                    ["Peak AQI", "Peak Time", "Safe Hours", "Danger Hours"],
                    [aqc(pred["peak_aqi"]), T['orange'], T['green'], T['red']],
                ):
                    with col_item:
                        st.markdown(f'<div class="stat"><div class="v" style="color:{vc}">{val}</div><div class="l">{lbl}</div></div>', unsafe_allow_html=True)

            fires = st.session_state.fires
            if fires is not None and not fires.empty:
                nearest = fires.sort_values("distance_km").iloc[0]
                d = nearest.get("distance_km", 0)
                st.markdown(f'<div class="al al-d" style="margin-top:18px"><strong>{len(fires)} active fire(s)</strong> within 300km of {city}. Nearest: <strong>{d:.0f} km</strong>. AQI spike expected in ~<strong>{max(1, int(d / 40))}h</strong>.</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — 72H PREDICTION
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "72H Prediction":
    st.markdown('<div class="sh">72-Hour AQI Prediction</div>', unsafe_allow_html=True)
    if st.session_state.prediction is None:
        nodata("Prediction requires real PM2.5 data from API + weather forecast. PM2.5 may not be available for this location.")
    else:
        pred = st.session_state.prediction
        city = st.session_state.city
        al = pred["aqi"]
        ts = pred["times"]
        pi = pred["peak_hour_idx"]
        cs = [aqc(a) for a in al]
        fig = go.Figure()
        fig.add_hrect(y0=200, y1=max(al) * 1.1, fillcolor="rgba(239,68,68,0.04)", line_width=0)
        fig.add_hrect(y0=100, y1=200, fillcolor="rgba(234,179,8,0.02)", line_width=0)
        fig.add_trace(go.Scatter(x=ts, y=al, mode="lines", line=dict(color=T['accent'], width=2.5, shape="spline"),
                                 fill="tozeroy", fillcolor="rgba(59,130,246,0.06)"))
        fig.add_trace(go.Scatter(x=ts, y=al, mode="markers", marker=dict(color=cs, size=5, line=dict(color=T["bg"], width=1)), showlegend=False))
        fig.add_trace(go.Scatter(x=[ts[pi]], y=[al[pi]], mode="markers+text", marker=dict(color=T['red'], size=14, symbol="star"),
                                 text=[f"PEAK: {al[pi]}"], textposition="top center", textfont=dict(color=T['red'], size=11)))
        fig.add_hline(y=150, line_dash="dot", line_color=T['red'], annotation_text="WHO Emergency", annotation_font_color=T['red'])
        fig.update_layout(title=f"72h AQI — {city}", height=400, xaxis_title="Time", yaxis_title="AQI", showlegend=False, **PL)
        st.plotly_chart(fig, use_container_width=True)

        ca, cb_col = st.columns(2)
        with ca:
            st.markdown("#### Safe Windows")
            sw = []
            i = 0
            while i < len(al):
                if al[i] <= 100:
                    s = ts[i]
                    while i < len(al) and al[i] <= 100:
                        i += 1
                    sw.append(f"{s[11:16]} → {ts[i - 1][11:16]}")
                else:
                    i += 1
            for w in sw[:5]:
                st.markdown(f'<div class="tip">{w}</div>', unsafe_allow_html=True)
            if not sw:
                st.markdown('<div class="al al-d">No safe windows. Stay indoors.</div>', unsafe_allow_html=True)
        with cb_col:
            st.markdown("#### Danger Windows")
            dw = []
            i = 0
            while i < len(al):
                if al[i] > 200:
                    s = ts[i]
                    while i < len(al) and al[i] > 200:
                        i += 1
                    dw.append((s, ts[i - 1], max(al[max(0, i - 5):i])))
                else:
                    i += 1
            for s, e, pk in dw[:5]:
                st.markdown(f'<div class="al al-d">{s[11:16]} → {e[11:16]} — Peak {pk}</div>', unsafe_allow_html=True)
            if not dw:
                st.markdown('<div class="al al-s">No extreme danger predicted.</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — HEATMAP
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "Pollution Heatmap":
    st.markdown('<div class="sh">Hyperlocal Pollution Heatmap</div>', unsafe_allow_html=True)
    lat, lon = st.session_state.lat, st.session_state.lon
    if lat is None:
        nodata("Location not detected.")
    else:
        try:
            import folium
            from streamlit_folium import st_folium
            m = folium.Map(location=[lat, lon], zoom_start=9, tiles=T["map_tiles"])
            ad = st.session_state.aqi_data
            if ad and ad.get("aqi") is not None:
                folium.Marker(
                    [lat, lon], tooltip=f"{st.session_state.city} — AQI {ad['aqi']}",
                    icon=folium.Icon(color="red", icon="cloud"),
                ).add_to(m)
            fires = st.session_state.fires
            if fires is not None and not fires.empty:
                for _, row in fires.iterrows():
                    folium.CircleMarker(
                        [row.get("latitude", lat), row.get("longitude", lon)],
                        radius=6, color="orange", fill=True, fill_opacity=0.7,
                        tooltip=f"Fire | {row.get('distance_km', 0):.0f} km",
                    ).add_to(m)
            st_folium(m, width="100%", height=500)
            if fires is not None and not fires.empty:
                nearest = fires.sort_values("distance_km").iloc[0]
                st.markdown(f'<div class="al al-d"><strong>{len(fires)} fire(s)</strong> within 300km. Nearest: {nearest.get("distance_km", 0):.0f} km</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="al al-s">No active fires within 300 km</div>', unsafe_allow_html=True)
        except ImportError:
            st.error("Install folium: pip install folium streamlit-folium")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — HEALTH RISK
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "Health Risk":
    st.markdown('<div class="sh">Personal Health Risk Calculator</div>', unsafe_allow_html=True)
    ad = st.session_state.aqi_data
    if ad is None or ad.get("aqi") is None:
        nodata("Health risk requires real AQI data. Could not fetch AQI for this location.")
    else:
        aq = ad["aqi"]
        p25 = ad.get("pm25")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="card"><b>Your Profile</b></div>', unsafe_allow_html=True)
            age = st.slider("Age", 1, 90, 28)
            smoker = st.checkbox("Smoker")
            asthma = st.checkbox("Asthma/COPD")
            heart = st.checkbox("Heart disease")
            outdoor_h = st.slider("Hours outdoors/day", 0.0, 12.0, 2.0, 0.5)
        with c2:
            st.markdown('<div class="card"><b>Current Live Conditions</b></div>', unsafe_allow_html=True)
            st.metric("City AQI", aq)
            if p25 is not None:
                st.metric("PM2.5", f"{p25} µg/m³")
            else:
                st.caption("PM2.5 data not available from API")
            ov = st.number_input("Override AQI", 0, 500, int(aq))
        if st.button("Calculate Risk", type="primary", use_container_width=True):
            result = hc.calculate_health_risk(age=age, smoker=smoker, asthma=asthma, heart_disease=heart,
                                              outdoor_hours=outdoor_h, current_aqi=int(ov), pm25=p25)
            sc, rl, rc = result["score"], result["risk_level"], result["risk_color"]
            st.markdown(f"""<div class="card" style="border-top:3px solid {rc};text-align:center;margin:18px 0">
                <div class="bignum"><div class="value" style="color:{rc}">{sc}</div>
                <div class="label" style="color:{rc};font-size:1rem">{rl} RISK</div>
                <div class="meta">You are <b style="color:{rc}">{result['multiplier']}x</b> more at risk than average</div></div>
            </div>""", unsafe_allow_html=True)
            r1, r2 = st.columns(2)
            with r1:
                st.markdown("#### Risk Factors")
                for factor in result["risk_factors"]:
                    st.markdown(f'<div class="tip">{factor}</div>', unsafe_allow_html=True)
            with r2:
                st.markdown("#### Advice")
                for tip in result["tips"]:
                    st.markdown(f'<div class="tip">{tip}</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — CITY COMPARISON
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "City Comparison":
    st.markdown('<div class="sh">Multi-City AQI Comparison</div>', unsafe_allow_html=True)
    cs = st.text_input("Enter up to 5 cities (comma-separated)", placeholder="e.g. Delhi, Mumbai, Hyderabad")
    cl = [x.strip() for x in cs.split(",") if x.strip()][:5]
    if st.button("Compare", type="primary"):
        with st.spinner("Fetching live AQI data..."):
            st.session_state.multi_cities = df_mod.get_multi_city_data(cl, WAQI_TOKEN)
    mc = st.session_state.multi_cities
    if mc:
        ms = sorted([x for x in mc if x.get("aqi") is not None], key=lambda x: x.get("aqi", 0), reverse=True)
        if not ms:
            nodata("Could not fetch real AQI data for any of those cities.")
        else:
            cols = st.columns(len(ms))
            medals = ["1st", "2nd", "3rd", "4th", "5th"]
            for i, cd in enumerate(ms):
                av = cd.get("aqi", 0)
                clr = aqc(av)
                with cols[i]:
                    st.markdown(f'<div class="stat" style="border-top:3px solid {clr}"><div style="font-size:0.72rem;color:{T["text3"]}">{medals[i]}</div><div class="v" style="color:{clr}">{av}</div><div class="l">{cd.get("city_name","")}</div></div>', unsafe_allow_html=True)
            fig = go.Figure(go.Bar(
                x=[x["city_name"] for x in ms], y=[x.get("aqi", 0) for x in ms],
                marker_color=[aqc(x.get("aqi", 0)) for x in ms],
                text=[x.get("aqi", 0) for x in ms], textposition="auto",
            ))
            fig.update_layout(title="AQI by City", height=350, **PL)
            st.plotly_chart(fig, use_container_width=True)
            sf = ms[-1]
            st.markdown(f'<div class="al al-s"><strong>{sf["city_name"]}</strong> is safest — AQI {sf.get("aqi","—")}</div>', unsafe_allow_html=True)
    elif cs:
        nodata("Enter cities and click Compare to fetch data.")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 6 — HOSPITAL ALERT
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "Hospital Alert":
    st.markdown('<div class="sh">Hospital Preparedness Dashboard</div>', unsafe_allow_html=True)
    if st.session_state.prediction is None:
        nodata("Hospital alert requires 72h prediction, which needs real PM2.5 data from API.")
    else:
        pop = st.number_input("City Population (Lakhs)", 1.0, 300.0, 50.0)
        hr = hp.predict_hospital_load(st.session_state.prediction["aqi"], population_lakhs=pop)
        ac = hr["alert_color"]
        st.markdown(f"""<div class="card" style="border-top:3px solid {ac};text-align:center;margin-bottom:20px">
            <div class="bignum"><div style="font-size:0.78rem;color:{T['text3']}">72-Hour Hospital Alert</div>
            <div class="value" style="color:{ac}">{hr['alert_level']}</div>
            <div class="meta">Max AQI (24h): <b style="color:{ac}">{hr['max_aqi_24h']}</b></div></div>
        </div>""", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.metric("Peak Patients/hr", hr["peak_patients_per_hour"])
        c2.metric("Total 72h Patients", hr["total_72h_patients"])
        c3.metric("Beds Needed", hr["recommended_beds"])
        fig = go.Figure(go.Scatter(
            x=st.session_state.prediction["times"], y=hr["hourly_patients"],
            mode="lines", fill="tozeroy", line=dict(color=T['red'], width=2),
            fillcolor="rgba(239,68,68,0.06)",
        ))
        fig.update_layout(title=f"Projected Respiratory Patients — {st.session_state.city}", height=350, yaxis_title="Patients/hr", **PL)
        st.plotly_chart(fig, use_container_width=True)
        ca, cb_col = st.columns(2)
        with ca:
            st.markdown("#### Medicines to Stock")
            for med in hr["medicines"]:
                st.markdown(f'<div class="tip">{med}</div>', unsafe_allow_html=True)
        with cb_col:
            st.markdown("#### Staff Recommendations")
            for rec in hr["staff_recommendations"]:
                st.markdown(f'<div class="tip">{rec}</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 7 — HISTORICAL TRENDS
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "Historical Trends":
    st.markdown('<div class="sh">30-Day Historical Analysis</div>', unsafe_allow_html=True)
    lat, lon, city = st.session_state.lat, st.session_state.lon, st.session_state.city
    if lat is None:
        nodata("Location not detected.")
    else:
        with st.spinner("Fetching historical weather data from Open-Meteo..."):
            hdf = df_mod.get_historical_weather(lat, lon, days=30)
        if hdf.empty:
            nodata("Could not load historical weather data from Open-Meteo.")
        else:
            hdf["est_pm25"] = (60 + (hdf["relativehumidity_2m"] - 50) * 0.8 - hdf["windspeed_10m"] * 2.5).clip(5, 400)
            hdf["est_aqi"] = hdf["est_pm25"].apply(df_mod.pm25_to_aqi)
            hdf["date"] = pd.to_datetime(hdf["time"]).dt.date
            hdf["hour"] = pd.to_datetime(hdf["time"]).dt.hour
            hdf["day_name"] = pd.to_datetime(hdf["time"]).dt.day_name()
            daily = hdf.groupby("date")["est_aqi"].mean().reset_index()
            daily.columns = ["date", "avg_aqi"]

            st.markdown('<div class="al al-i"><strong>Note:</strong> AQI values are <b>estimated</b> from real historical weather data (wind speed, humidity) since free APIs don\'t provide historical AQI. Real-time AQI on other pages is from live API sensors.</div>', unsafe_allow_html=True)

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=daily["date"].astype(str), y=daily["avg_aqi"],
                mode="lines+markers", line=dict(color=T['accent'], width=2, shape="spline"),
                marker=dict(color=[aqc(a) for a in daily["avg_aqi"]], size=7),
            ))
            fig.add_hline(y=150, line_dash="dot", line_color=T['red'], annotation_text="Unhealthy", annotation_font_color=T['red'])
            fig.update_layout(title=f"30-Day Estimated AQI — {city} (weather-based)", height=380, **PL)
            st.plotly_chart(fig, use_container_width=True)

            c1, c2 = st.columns(2)
            with c1:
                st.markdown("#### By Day of Week")
                dow = hdf.groupby("day_name")["est_aqi"].mean().reindex(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
                fig2 = px.bar(x=dow.index, y=dow.values, color=dow.values, color_continuous_scale="RdYlGn_r", labels={"x":"Day","y":"Est. AQI"})
                fig2.update_layout(height=300, coloraxis_showscale=False, **PL)
                st.plotly_chart(fig2, use_container_width=True)
            with c2:
                st.markdown("#### By Hour of Day")
                ha = hdf.groupby("hour")["est_aqi"].mean()
                fig3 = px.line(x=ha.index, y=ha.values, labels={"x":"Hour","y":"Est. AQI"})
                fig3.update_traces(line_color=T['accent'])
                fig3.update_layout(height=300, **PL)
                st.plotly_chart(fig3, use_container_width=True)

            wd = daily.loc[daily["avg_aqi"].idxmax()]
            bd = daily.loc[daily["avg_aqi"].idxmin()]
            st.markdown(f'<div class="card"><strong>Worst:</strong> {wd["date"]} — Est. AQI {int(wd["avg_aqi"])}<br><strong>Best:</strong> {bd["date"]} — Est. AQI {int(bd["avg_aqi"])}</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 8 — GREEN TRACKER
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "Green Tracker":
    st.markdown('<div class="sh">Green Action Tracker</div>', unsafe_allow_html=True)
    GA = {
        "Used public transport": (20, 2.1), "Cycled/walked": (25, 1.8),
        "Planted a tree": (50, 0.06), "Ate vegetarian": (15, 1.5),
        "Turned off electronics": (10, 0.4), "Reduced AC 2+ hrs": (12, 2.4),
        "Carpooled": (18, 1.6), "Recycled waste": (10, 0.3),
        "Used cloth bag": (8, 0.1), "Avoided burning waste": (30, 3.0),
    }
    tp = st.session_state.green_points
    log = st.session_state.green_log
    tc = sum(e.get("co2", 0) for e in log)
    for col_item, val, lbl, vc in zip(
        st.columns(3),
        [str(tp), f"{tc:.1f} kg", f"{tc / 22:.3f}"],
        ["Points", "CO2 Saved", "Trees Equiv."],
        [T['accent'], T['green'], T['green']],
    ):
        with col_item:
            st.markdown(f'<div class="stat"><div class="v" style="color:{vc}">{val}</div><div class="l">{lbl}</div></div>', unsafe_allow_html=True)
    if tp >= 200: rk = "Eco Champion"
    elif tp >= 100: rk = "Green Warrior"
    elif tp >= 50: rk = "Eco Starter"
    else: rk = "Beginner"
    st.markdown(f'<div style="text-align:center;color:{T["green"]};font-weight:700;margin:12px 0">{rk}</div>', unsafe_allow_html=True)
    st.markdown("#### Log Actions")
    for act, (pts, co2) in GA.items():
        ca, cb_col = st.columns([4, 1])
        with ca:
            st.markdown(f'<div class="tip">{act} — <b style="color:{T["green"]}">+{pts} pts</b> | {co2} kg CO2</div>', unsafe_allow_html=True)
        with cb_col:
            if st.button("Log", key=f"g_{act[:10]}"):
                st.session_state.green_points += pts
                st.session_state.green_log.append({"action": act, "points": pts, "co2": co2, "time": datetime.now().strftime("%H:%M")})
                st.rerun()
    if log:
        st.markdown("#### Activity Log")
        st.dataframe(pd.DataFrame(log)[["time", "action", "points", "co2"]], use_container_width=True, hide_index=True)
    if st.button("Reset"):
        st.session_state.green_points = 0
        st.session_state.green_log = []
        st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 9 — CARBON CALCULATOR
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "Carbon Calculator":
    st.markdown('<div class="sh">Carbon Footprint Calculator</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="card"><b>Transport</b></div>', unsafe_allow_html=True)
        car = st.slider("Car km/day", 0, 100, 0)
        bike = st.slider("2-Wheeler km/day", 0, 80, 0)
        auto = st.slider("Auto/Cab km/day", 0, 50, 0)
        bus = st.slider("Bus km/day", 0, 80, 0)
        metro = st.slider("Metro km/day", 0, 80, 0)
        flights = st.slider("Flights/year", 0, 30, 0)
    with c2:
        st.markdown('<div class="card"><b>Home Energy</b></div>', unsafe_allow_html=True)
        ac_hrs = st.slider("AC hrs/day", 0.0, 24.0, 0.0, 0.5)
        elec = st.slider("Electricity units/day", 0.0, 30.0, 0.0, 0.5)
        lpg = st.slider("LPG cylinders/month", 0.0, 5.0, 0.0, 0.5)
        st.markdown('<div class="card"><b>Diet</b></div>', unsafe_allow_html=True)
        diet = st.radio("Diet", ["vegetarian", "non-vegetarian"], horizontal=True)
    if st.button("Calculate", type="primary", use_container_width=True):
        result = cc.calculate_carbon(
            car_km_day=car, bike_km_day=bike, auto_km_day=auto,
            bus_km_day=bus, metro_km_day=metro, flights_per_year=flights,
            ac_hours_day=ac_hrs, units_electricity_day=elec,
            lpg_cylinders_month=lpg, diet=diet)
        total = result["total_daily_kg"]
        an = result["annual_tonnes"]
        vi = result["vs_india_average"]
        bc = T['red'] if vi > 1.5 else T['orange'] if vi > 1.0 else T['green']
        st.markdown(f"""<div class="card" style="border-top:3px solid {bc};text-align:center;margin:18px 0">
            <div class="bignum"><div class="value" style="color:{bc}">{total} kg</div>
            <div class="label">CO2/day | <b style="color:{bc}">{an} t/yr</b></div>
            <div class="meta"><b style="color:{bc}">{vi}x</b> India average</div></div>
        </div>""", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.metric("Daily", f"{total} kg")
        c2.metric("Annual", f"{an} t")
        c3.metric("Trees", f"{result['trees_needed']:,}")
        bd = result["breakdown"]
        fig = go.Figure(go.Pie(
            labels=list(bd.keys()), values=list(bd.values()), hole=0.45,
            marker_colors=[T['red'], T['orange'], T['yellow'], T['green'], T['accent'], "#a855f7"][:len(bd)],
        ))
        fig.update_layout(title="Breakdown", height=380, **PL)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f"**Biggest contributor:** {result['biggest_contributor']}")
        for tip in result["tips"]:
            st.markdown(f'<div class="tip">{tip}</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 10 — AI CHATBOT
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "AI Chatbot":
    st.markdown('<div class="sh">VAYU AI Assistant</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="al al-i">Powered by <b>NVIDIA Kimi K2</b> AI · Ask anything about pollution, health risks, masks, or safety tips for <b>{st.session_state.city}</b></div>', unsafe_allow_html=True)

    cb.init_chat_session()

    st.markdown(f'<div style="font-size:0.78rem;color:{T["text3"]};margin:14px 0 8px">Quick questions:</div>', unsafe_allow_html=True)
    quick_qs = [
        "Is it safe to exercise outdoors today?",
        "What mask should I buy for this AQI?",
        "How to protect my child from pollution?",
        "Why is pollution so high right now?",
    ]
    qcols = st.columns(len(quick_qs))
    for i, qq in enumerate(quick_qs):
        with qcols[i]:
            if st.button(qq, key=f"qq_{i}", use_container_width=True):
                ad = st.session_state.aqi_data or {"aqi": "unknown"}
                cb.add_user_message(qq)
                with st.spinner("VAYU is thinking..."):
                    response = cb.get_chat_response(qq, st.session_state.city, ad)
                cb.add_bot_message(response)
                st.rerun()

    st.markdown("---")
    cb.render_chat_messages()

    user_input = st.chat_input(f"Ask VAYU about pollution in {st.session_state.city}...")
    if user_input:
        ad = st.session_state.aqi_data or {"aqi": "unknown"}
        cb.add_user_message(user_input)
        with st.chat_message("user"):
            st.markdown(user_input)
        with st.chat_message("assistant"):
            with st.spinner("VAYU is thinking..."):
                response = cb.get_chat_response(user_input, st.session_state.city, ad)
            st.markdown(response)
        cb.add_bot_message(response)

    if st.session_state.vayu_chat_history:
        if st.button("Clear Chat", key="clear_chat"):
            cb.clear_chat()
            st.rerun()

# ─── Footer ────────────────────────────────────────────────────────────────────
st.markdown(f"""<div class="foot">
    <b style="color:{T['text']}">VAYU AI</b> — Hack For Green Bharat 2026<br>
    OpenAQ · Open-Meteo · NASA FIRMS · WAQI · OpenStreetMap · NVIDIA Kimi K2<br>
    <i>16 lakh Indians die from pollution yearly. VAYU warns 72h ahead.</i>
</div>""", unsafe_allow_html=True)
