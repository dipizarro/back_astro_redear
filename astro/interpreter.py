import json

with open("astro/data/meanings.json", "r", encoding="utf-8") as f:
    MEANINGS = json.load(f)

def interpret(positions):
    sun_sign = "aries"  # Aquí harías la conversión real
    moon_sign = "pisces"

    return {
        "sun": MEANINGS["sun"].get(sun_sign, ""),
        "moon": MEANINGS["moon"].get(moon_sign, "")
    }

