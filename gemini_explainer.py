"""
gemini_explainer.py — VAYU AI
AI integration using NVIDIA Kimi K2 API.
NO FAKE DATA. NO PREDEFINED RESPONSES. NO FALLBACKS.
If NVIDIA API is unavailable, we return a clear error — never fabricated text.
"""

import logging
import requests

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are VAYU, an expert AI assistant specialized in air pollution, environmental health, and public safety in India.
You are given real-time pollution data for the user's city. Always base your answer strictly on this data.
Be direct, factual, and urgent when danger is high. Use simple English for common people.
Do NOT use emojis. No markdown headers with #. Use plain paragraphs and bold text only.
Never guess or speculate beyond the data given. If you don't know, say so clearly.
Always end with one specific action the person should take right now."""

NVIDIA_API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
NVIDIA_API_KEY = "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"
NVIDIA_MODEL = "moonshotai/kimi-k2-instruct-0905"

_initialized = False


def init_ai(api_key: str = None) -> bool:
    global _initialized, NVIDIA_API_KEY
    if api_key and api_key.strip() not in ("", "YOUR_API_KEY"):
        NVIDIA_API_KEY = api_key.strip()
    if NVIDIA_API_KEY and NVIDIA_API_KEY.startswith("nvapi-"):
        _initialized = True
        return True
    logger.warning("No valid NVIDIA API key.")
    return False


init_ai()


def _call_nvidia(messages: list, max_tokens: int = 1200) -> str:
    """Call NVIDIA Kimi K2 API. Returns response text, or None on failure."""
    if not _initialized:
        return None
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {NVIDIA_API_KEY}",
        }
        payload = {
            "model": NVIDIA_MODEL,
            "messages": messages,
            "temperature": 0.5,
            "top_p": 0.9,
            "max_tokens": max_tokens,
            "stream": False,
        }
        resp = requests.post(NVIDIA_API_URL, headers=headers, json=payload, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        else:
            logger.warning(f"NVIDIA API {resp.status_code}: {resp.text[:200]}")
            return None
    except Exception as e:
        logger.warning(f"NVIDIA API call failed: {e}")
        return None


def _city_context(city: str, aqi_data: dict) -> str:
    """Build a context string from real live data."""
    aqi = aqi_data.get("aqi", "unavailable")
    pm25 = aqi_data.get("pm25", "unavailable")
    pm10 = aqi_data.get("pm10", "unavailable")
    no2 = aqi_data.get("no2", "unavailable")
    co = aqi_data.get("co", "unavailable")
    src = aqi_data.get("source", "live sensor")
    ts = aqi_data.get("timestamp", "")[:16]
    return (
        f"[REAL-TIME DATA from {src} at {ts}]\n"
        f"City: {city}\n"
        f"AQI: {aqi}\n"
        f"PM2.5: {pm25} µg/m³ (WHO safe limit: 15)\n"
        f"PM10: {pm10} µg/m³ (WHO safe limit: 45)\n"
        f"NO2: {no2} µg/m³\n"
        f"CO: {co} mg/m³"
    )


def explain_pollution(city: str, aqi_data: dict, weather: dict = None) -> str:
    """Generate real AI explanation of current pollution conditions using NVIDIA Kimi K2."""
    context = _city_context(city, aqi_data)
    weather_str = ""
    if weather:
        ws = weather.get("windspeed_10m", [None])[0]
        hum = weather.get("relativehumidity_2m", [None])[0]
        temp = weather.get("temperature_2m", [None])[0]
        if ws is not None:
            weather_str = f"\nWeather: Wind {ws} km/h, Humidity {hum}%, Temp {temp}°C"

    prompt = (
        f"{context}{weather_str}\n\n"
        f"Based ONLY on the real data above, explain in 3 short paragraphs:\n"
        f"1. Why is pollution at this exact level in {city} right now?\n"
        f"2. What specific health risks do people face at AQI {aqi_data.get('aqi','this level')}?\n"
        f"3. What one specific action must they take immediately?"
    )
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]
    result = _call_nvidia(messages)
    if result:
        return result
    return f"NVIDIA AI is currently unavailable. Live AQI for {city}: {aqi_data.get('aqi', 'N/A')}. Check the dashboard for real-time data."


def chat_with_vayu(history: list, question: str, city: str, aqi_data: dict) -> str:
    """
    Chat with VAYU using real NVIDIA Kimi K2 AI.
    All responses are generated live by the AI — NO predefined text.
    Returns AI response, or a clear error if API is unreachable.
    """
    context = _city_context(city, aqi_data)
    augmented_question = (
        f"{context}\n\n"
        f"User question: {question}"
    )

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Include last 8 turns of real conversation history
    for msg in history[-8:]:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        if role in ("user", "assistant") and content:
            messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": augmented_question})

    result = _call_nvidia(messages, max_tokens=1200)
    if result:
        return result

    # Return a clean error — not a fake predefined answer
    return (
        f"The NVIDIA AI service is temporarily unavailable (network issue or rate limit). "
        f"Live data shows {city} AQI = {aqi_data.get('aqi', 'N/A')}, "
        f"PM2.5 = {aqi_data.get('pm25', 'N/A')} µg/m³. "
        f"Please try again in a moment."
    )
