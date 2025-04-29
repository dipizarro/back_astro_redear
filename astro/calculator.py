from skyfield.api import load, Topos
from datetime import datetime
from pytz import timezone as tz
import ephem
import math

SIGNS = [
    "aries", "taurus", "gemini", "cancer",
    "leo", "virgo", "libra", "scorpio",
    "sagittarius", "capricorn", "aquarius", "pisces"
]

PLANETS = {
    "sun": "sun",
    "moon": "moon",
    "mercury": "mercury",
    "venus": "venus",
    "mars": "mars",
    "jupiter": "jupiter barycenter",
    "saturn": "saturn barycenter",
    "uranus": "uranus barycenter",
    "neptune": "neptune barycenter",
    "pluto": "pluto barycenter"
}

def get_sign_from_degrees(degrees):
    index = int(degrees / 30) % 12
    return SIGNS[index]

def parse_datetime(date_str: str) -> datetime:
    try:
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except ValueError:
        return datetime.strptime(date_str, "%Y/%m/%d %H:%M").replace(tzinfo=tz('UTC'))

def get_planet_positions(date_str, latitude, longitude):
    dt = parse_datetime(date_str)

    latitude = float(latitude)
    longitude = float(longitude)

    ts = load.timescale()
    t = ts.utc(dt)

    eph = load('de421.bsp')
    observer = eph['earth'] + Topos(latitude_degrees=latitude, longitude_degrees=longitude)

    positions = {}

    # Planets
    for name, skyfield_name in PLANETS.items():
        planet = eph[skyfield_name]
        astrometric = observer.at(t).observe(planet).apparent()
        ecl = astrometric.ecliptic_latlon()
        lon = ecl[1].degrees
        positions[name] = {
            "degree": round(lon, 2),
            "sign": get_sign_from_degrees(lon)
        }

    # Ascendant & Houses (simulados con grados distribuidos)
    asc_deg = positions["sun"]["degree"]  # como referencia provisional
    positions["ascendant"] = {
        "degree": round(asc_deg % 360, 2),
        "sign": get_sign_from_degrees(asc_deg)
    }

    positions["houses"] = {}
    for i in range(1, 13):
        house_deg = (asc_deg + (i - 1) * 30) % 360
        positions["houses"][f"house_{i}"] = {
            "degree": round(house_deg, 2),
            "sign": get_sign_from_degrees(house_deg)
        }

    return positions
