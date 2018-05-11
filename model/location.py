from geojson import Point


class Location:

    def __init__(self, latitude: float, longitude: float):

        if longitude < -180 or 180 < longitude:
            raise ValueError(
                'Longitude value have to be -180 <= longitude <= 180')

        if latitude < -90 or 90 < latitude:
            raise ValueError(
                'Latitude value have to be -90 <= latitude <= 90')

        self._point = Point((longitude, latitude))

    @property
    def longitude(self):
        return self._point['coordinates'][0]

    @property
    def latitude(self):
        return self._point['coordinates'][1]

    def get_geo_json_point(self):
        return self._point
