from geojson import Point


def get_location(postcode, admin_district, latitude, longitude):
    return {
        "postcode": postcode,
        "admin_district": admin_district,
        "geo_location": get_geo_location(latitude, longitude)
    }


def get_geo_location(latitude, longitude):
    return dict(Point((longitude, latitude)))


def validate_lat_long_values(latitude, longitude):
    if latitude < -90 or 90 < latitude:
        raise ValueError(
            'Latitude value have to be -90 <= latitude <= 90')

    if longitude < -180 or 180 < longitude:
        raise ValueError(
            'Longitude value have to be -180 <= longitude <= 180')
