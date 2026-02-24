"""
carbon_calculator.py — VAYU AI
Personal carbon footprint calculator with eco-tips.
"""


# CO2 emission factors (kg CO2 per unit)
EMISSION_FACTORS = {
    "petrol_car_per_km": 0.21,       # avg Indian car
    "diesel_car_per_km": 0.17,
    "two_wheeler_per_km": 0.09,
    "auto_rickshaw_per_km": 0.07,
    "bus_per_km": 0.04,
    "metro_per_km": 0.02,
    "flight_domestic_per_hour": 255,  # kg per hour (avg 130kg/h per passenger)
    "ac_per_hour": 1.2,              # 1.5 ton AC, India grid
    "electricity_per_unit": 0.82,    # India average kg CO2/kWh
    "non_veg_per_day": 7.2,         # kg CO2e per day
    "veg_per_day": 2.5,
    "lpg_per_cylinder": 12.0,        # 14.2kg LPG
}

INDIA_AVERAGE_ANNUAL_KG = 1900           # ~1.9 tonnes CO2 per person per year
INDIA_AVERAGE_DAILY_KG = INDIA_AVERAGE_ANNUAL_KG / 365
GLOBAL_AVERAGE_DAILY_KG = 12_000 / 365  # ~4 tonnes/year global avg


def calculate_carbon(
    car_km_day: float = 0,
    bike_km_day: float = 0,
    auto_km_day: float = 0,
    bus_km_day: float = 0,
    metro_km_day: float = 0,
    flights_per_year: int = 0,
    avg_flight_duration_h: float = 2.0,
    ac_hours_day: float = 0,
    units_electricity_day: float = 3.0,
    lpg_cylinders_month: float = 1.0,
    diet: str = "non-vegetarian",
) -> dict:
    """
    Calculate daily personal carbon footprint in kg CO2.
    Returns detailed breakdown dict.
    """
    # Daily transport
    transport_car = car_km_day * EMISSION_FACTORS["petrol_car_per_km"]
    transport_bike = bike_km_day * EMISSION_FACTORS["two_wheeler_per_km"]
    transport_auto = auto_km_day * EMISSION_FACTORS["auto_rickshaw_per_km"]
    transport_bus = bus_km_day * EMISSION_FACTORS["bus_per_km"]
    transport_metro = metro_km_day * EMISSION_FACTORS["metro_per_km"]
    transport_total = transport_car + transport_bike + transport_auto + transport_bus + transport_metro

    # Flights (amortised daily)
    flights_daily = (flights_per_year * avg_flight_duration_h * EMISSION_FACTORS["flight_domestic_per_hour"]) / 365
    
    # Home energy
    ac_daily = ac_hours_day * EMISSION_FACTORS["ac_per_hour"]
    electricity_daily = units_electricity_day * EMISSION_FACTORS["electricity_per_unit"]
    lpg_daily = (lpg_cylinders_month * EMISSION_FACTORS["lpg_per_cylinder"]) / 30
    home_total = ac_daily + electricity_daily + lpg_daily

    # Diet
    diet_daily = EMISSION_FACTORS["non_veg_per_day"] if diet.lower() == "non-vegetarian" else EMISSION_FACTORS["veg_per_day"]

    total_daily_kg = transport_total + flights_daily + home_total + diet_daily
    annual_kg = total_daily_kg * 365

    # Trees to offset (one tree absorbs ~22 kg CO2/year)
    trees_needed = round(annual_kg / 22)

    # vs India average
    vs_india = round(total_daily_kg / INDIA_AVERAGE_DAILY_KG, 1)

    # Biggest contributor
    categories = {
        "Transport (Car)": transport_car,
        "Transport (Bike)": transport_bike,
        "Transport (Auto/Taxi)": transport_auto,
        "Transport (Bus)": transport_bus,
        "Transport (Metro)": transport_metro,
        "Flights": flights_daily,
        "Air Conditioning": ac_daily,
        "Electricity": electricity_daily,
        "LPG / Cooking": lpg_daily,
        "Diet": diet_daily,
    }
    categories_nonzero = {k: round(v, 3) for k, v in categories.items() if v > 0}
    biggest = max(categories_nonzero, key=categories_nonzero.get) if categories_nonzero else "Diet"

    # Tips
    tips = _generate_tips(
        car_km_day, bike_km_day, ac_hours_day, diet,
        flights_per_year, transport_car, diet_daily, ac_daily
    )

    return {
        "total_daily_kg": round(total_daily_kg, 2),
        "annual_kg": round(annual_kg, 1),
        "annual_tonnes": round(annual_kg / 1000, 2),
        "trees_needed": trees_needed,
        "vs_india_average": vs_india,
        "breakdown": categories_nonzero,
        "biggest_contributor": biggest,
        "tips": tips,
        "india_avg_daily": round(INDIA_AVERAGE_DAILY_KG, 2),
        "global_avg_daily": round(GLOBAL_AVERAGE_DAILY_KG, 2),
    }


def _generate_tips(car_km, bike_km, ac_h, diet, flights, car_co2, diet_co2, ac_co2):
    tips = []
    if car_km > 10:
        saved = (car_km - 0) * (EMISSION_FACTORS["petrol_car_per_km"] - EMISSION_FACTORS["metro_per_km"])
        tips.append(f"🚇 Switch {car_km:.0f} km/day car commute to metro → save **{saved:.1f} kg CO2/day** ({saved*365:.0f} kg/year)")
    if bike_km > 5:
        tips.append(f"🚲 Replace short 2-wheeler trips with cycling → zero emissions + better health")
    if ac_h > 4:
        saved_ac = (ac_h - 2) * EMISSION_FACTORS["ac_per_hour"]
        tips.append(f"❄️ Reduce AC to 26°C and use for 2 fewer hours → save **{saved_ac:.1f} kg CO2/day**")
    if diet.lower() == "non-vegetarian":
        saved_diet = diet_co2 - EMISSION_FACTORS["veg_per_day"]
        tips.append(f"🥦 Try 2 vegetarian days/week → save **{saved_diet * 2 / 7:.1f} kg CO2/day** ({saved_diet * 2 * 52:.0f} kg/year)")
    if flights > 2:
        tips.append(f"✈️ Replace 1 domestic flight with train → saves ~200 kg CO2 per trip")
    tips.append("💡 Switch to LED bulbs → reduces lighting energy by 75%")
    tips.append("🌱 Plant 5 trees → offset ~110 kg CO2/year naturally")
    return tips[:5]
