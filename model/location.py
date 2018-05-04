from geojson import Point


class Location:

    def __init__(self, lng: float, lat: float):

        if lng < -180 or 180 < lng:
            raise ValueError(
                'Longitude value have to be -180 <= longitude <= 180')

        if lat < -90 or 90 < lat:
            raise ValueError(
                'Latitude value have to be -90 <= latitude <= 90')

        self._point = Point((lng, lat))

    @property
    def longitude(self):
        return self._point['coordinates'][0]

    @property
    def latitude(self):
        return self._point['coordinates'][1]

    def get_geo_json_point(self):
        return self._point
