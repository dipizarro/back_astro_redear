from skyfield.api import load, Topos, utc
from skyfield.almanac import risings_and_settings, find_discrete
from datetime import datetime
from pytz import timezone as tz
import math
import numpy as np
import json

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

PLANET_TRANSLATE = {
    "sun": "sol",
    "moon": "luna",
    "mercury": "mercurio",
    "venus": "venus",
    "mars": "marte",
    "jupiter": "jupiter",
    "saturn": "saturno",
    "uranus": "urano",
    "neptune": "neptuno",
    "pluto": "pluton"
}

ASPECTS = [
    {"name": "conjunción", "angle": 0, "orb": 8},
    {"name": "oposición", "angle": 180, "orb": 8},
    {"name": "trígono", "angle": 120, "orb": 6},
    {"name": "cuadratura", "angle": 90, "orb": 6},
    {"name": "sextil", "angle": 60, "orb": 4}
]


def get_sign_from_degrees(degrees):
    index = int(degrees / 30) % 12
    return SIGNS[index]

def parse_datetime(date_str):
    # Espera formato ISO: YYYY-MM-DDTHH:MM:SS o similar
    dt = datetime.fromisoformat(date_str)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=utc)
    return dt

def get_ascendant_and_houses(ts, eph, dt, latitude, longitude):
    from skyfield.api import wgs84
    from skyfield.positionlib import ICRF
    from skyfield import almanac
    
    observer = wgs84.latlon(latitude, longitude)
    t = ts.utc(dt)
    earth = eph['earth']
    loc = earth + observer
    
    # Cálculo del Ascendente
    astrometric = loc.at(t).observe(eph['sun'])
    apparent = astrometric.apparent()
    ra, dec, distance = apparent.radec()
    lst = t.gmst + longitude / 15.0
    obliquity = 23.43929111  # oblicuidad eclíptica media
    asc_rad = math.atan2(
        -math.cos(math.radians(obliquity)) * math.tan(math.radians(latitude)),
        math.sin(math.radians(lst * 15))
    )
    asc_deg = (math.degrees(asc_rad) + 360) % 360
    asc_sign = get_sign_from_degrees(asc_deg)
    
    # Cálculo simple de casas (igual de 30° desde el ascendente)
    houses = {}
    for i in range(1, 13):
        house_deg = (asc_deg + (i - 1) * 30) % 360
        houses[f"house_{i}"] = {
            "degree": round(house_deg, 2),
            "sign": get_sign_from_degrees(house_deg)
        }
    return asc_deg, asc_sign, houses

def calculate_aspects(positions):
    aspects = []
    planet_names = [k for k in positions.keys() if k in PLANETS]
    for i, p1 in enumerate(planet_names):
        deg1 = positions[p1]["degree"]
        for j in range(i+1, len(planet_names)):
            p2 = planet_names[j]
            deg2 = positions[p2]["degree"]
            diff = abs(deg1 - deg2)
            diff = min(diff, 360 - diff)  # ángulo menor
            for asp in ASPECTS:
                if abs(diff - asp["angle"]) <= asp["orb"]:
                    aspects.append({
                        "planet1": p1,
                        "planet2": p2,
                        "aspect": asp["name"],
                        "angle": round(diff, 2)
                    })
    return aspects

def get_aspect_interpretations(aspects):
    try:
        with open("astro/data/aspects.json", "r", encoding="utf-8") as f:
            aspect_meanings = json.load(f)
    except Exception:
        aspect_meanings = {}
    interpretations = []
    for asp in aspects:
        p1 = PLANET_TRANSLATE.get(asp["planet1"], asp["planet1"])
        p2 = PLANET_TRANSLATE.get(asp["planet2"], asp["planet2"])
        aspect_type = asp["aspect"]
        interp = None
        # Buscar interpretación directa o invertida
        if p1 in aspect_meanings and p2 in aspect_meanings[p1]:
            interp = aspect_meanings[p1][p2].get(aspect_type)
        elif p2 in aspect_meanings and p1 in aspect_meanings[p2]:
            interp = aspect_meanings[p2][p1].get(aspect_type)
        if interp:
            interpretations.append({
                "planet1": asp["planet1"],
                "planet2": asp["planet2"],
                "aspect": aspect_type,
                "interpretation": interp
            })
        else:
            interpretations.append({
                "planet1": asp["planet1"],
                "planet2": asp["planet2"],
                "aspect": aspect_type,
                "interpretation": f"No hay interpretación disponible para {asp['planet1']} {aspect_type} {asp['planet2']}."
            })
    return interpretations

def get_planet_positions(date_str, latitude, longitude):
    dt = parse_datetime(date_str)
    latitude = float(latitude)
    longitude = float(longitude)
    ts = load.timescale()
    t = ts.utc(dt)
    eph = load('de421.bsp')
    observer = eph['earth'] + Topos(latitude_degrees=latitude, longitude_degrees=longitude)
    positions = {}
    # Planetas
    for name, skyfield_name in PLANETS.items():
        planet = eph[skyfield_name]
        astrometric = observer.at(t).observe(planet).apparent()
        ecl = astrometric.ecliptic_latlon()
        lon = ecl[1].degrees
        positions[name] = {
            "degree": round(lon, 2),
            "sign": get_sign_from_degrees(lon)
        }
    # Ascendente y casas reales
    asc_deg, asc_sign, houses = get_ascendant_and_houses(ts, eph, dt, latitude, longitude)
    positions["ascendant"] = {
        "degree": round(asc_deg, 2),
        "sign": asc_sign
    }
    positions["houses"] = houses
    # Aspectos planetarios
    positions["aspects"] = calculate_aspects(positions)
    positions["aspect_interpretations"] = get_aspect_interpretations(positions["aspects"])
    return positions
