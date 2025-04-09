from skyfield.api import load

def get_planet_positions(date, location):
    planets = load('de421.bsp')
    earth = planets['earth']
    observer = earth + location
    sun = planets['sun']

    astrometric = observer.at(date).observe(sun)
    ra, dec, distance = astrometric.radec()

    return {
        "sun_ra": str(ra),
        "sun_dec": str(dec)
    }
