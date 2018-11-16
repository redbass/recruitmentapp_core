import geopy.distance

EARTH_RADIUS_KM = 6371


def km2rad(km):
    return km / EARTH_RADIUS_KM


def get_coordinates_from_location(location):
    return [location.get('latitude'), location.get('longitude')]


def distance_from_location(current_location, location):
    coords = get_coordinates_from_location(location)
    return geopy.distance.vincenty(current_location, coords).km
