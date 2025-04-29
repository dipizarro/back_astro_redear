import json

default_profile = "profesional"

with open("astro/data/meanings.json", "r", encoding="utf-8") as f:
    MEANINGS = json.load(f)

def interpret(positions, interpretation_type="professional"):
    reading = {}

    # Planetas y Ascendente
    for key, pos in positions.items():
        if key in MEANINGS and isinstance(pos, dict) and "sign" in pos:
            sign = pos["sign"]
            planet_meaning = MEANINGS[key].get(sign, {})
            if isinstance(planet_meaning, dict):
                reading[key] = planet_meaning.get(interpretation_type, "Sin interpretación disponible.")
            else:
                reading[key] = planet_meaning  # para retrocompatibilidad

    # Casas
    if "houses" in positions:
        reading["houses"] = {}
        for full_key, house_data in positions["houses"].items():
            sign = house_data["sign"]
            house_number = full_key.replace("house_", "")
            house_interpretation = MEANINGS["houses"].get(house_number, {}).get(sign, {})

            if isinstance(house_interpretation, dict):
                reading["houses"][full_key] = house_interpretation.get(interpretation_type,
                                                                       "Sin interpretación disponible.")
            else:
                reading["houses"][full_key] = house_interpretation  # fallback retrocompatible

    return reading

