import json

default_profile = "profesional"

with open("astro/data/meanings.json", "r", encoding="utf-8") as f:
    MEANINGS = json.load(f)

def obtener_interpretacion(aspecto_dict, type="professional"):
    """
    Devuelve la interpretación según el perfil solicitado.
    Si no existe el perfil, devuelve un mensaje genérico.
    """
    if isinstance(aspecto_dict, dict):
        if type in aspecto_dict:
            return aspecto_dict[type]
        else:
            return "No hay interpretación disponible para este aspecto en el perfil seleccionado."
    elif isinstance(aspecto_dict, str):
        return aspecto_dict
    else:
        return "No hay interpretación disponible para este aspecto."


def interpret(positions, type="professional"):
    reading = {
        "identity": {},
        "personal_planets": {},
        "social_planets": {},
        "transpersonal_planets": {},
        "houses": {}
    }

    identity_keys = {"sun", "moon", "ascendant"}
    personal_keys = {"mercury", "venus", "mars"}
    social_keys = {"jupiter", "saturn"}
    transpersonal_keys = {"uranus", "neptune", "pluto"}

    for key, pos in positions.items():
        if key == "houses":
            continue

        if key in MEANINGS and isinstance(pos, dict) and "sign" in pos:
            sign = pos["sign"]
            planet_meaning = MEANINGS[key].get(sign, {})
            interpretacion = obtener_interpretacion(planet_meaning, type)
            structured = { "sign": sign, "interpretacion": interpretacion }

            if key in identity_keys:
                reading["identity"][key] = structured
            elif key in personal_keys:
                reading["personal_planets"][key] = structured
            elif key in social_keys:
                reading["social_planets"][key] = structured
            elif key in transpersonal_keys:
                reading["transpersonal_planets"][key] = structured

    if "houses" in positions:
        for full_key, house_data in positions["houses"].items():
            sign = house_data["sign"]
            house_number = full_key.replace("house_", "")
            house_interpretation = MEANINGS["houses"].get(house_number, {}).get(sign, {})
            interpretacion = obtener_interpretacion(house_interpretation, type)
            structured = { "sign": sign, "interpretacion": interpretacion }
            reading["houses"][full_key] = structured

    return reading
