from unittest import TestCase

from model.geo_location import get_location, validate_lat_long_values


class TestLocation(TestCase):

    def test_location(self):
        lat = 55.966758728026
        lng = -3.2203674316403
        admin_district = "test district"
        location = get_location("EH1 1HE", admin_district, lat, lng)

        geo_coordinates = self._get_geo_coordinates(location)

        self.assertEqual([lng, lat], geo_coordinates)

    def test_location_longitude_validity(self):

        valid_longitude = [-180, -90.1234, 0, 99.3333, 180]
        invalid_longitude = [-270, -181, -180.00000001, 180.0000001, 181, 270]

        for lng in valid_longitude:
            validate_lat_long_values(latitude=0, longitude=lng)

        for lng in invalid_longitude:
            with self.assertRaises(ValueError):
                validate_lat_long_values(latitude=0, longitude=lng)

    def test_location_latitude_validity(self):

        valid_latitudes = [-90, -45.1234, 0, 33.3333, 90]
        invalid_latitudes = [-180, -91, -90.0000000001, 90.000000001, 91, 180]

        for lat in valid_latitudes:
            validate_lat_long_values(latitude=lat, longitude=0)

        for lat in invalid_latitudes:
            with self.assertRaises(ValueError):
                validate_lat_long_values(latitude=lat, longitude=0)

    @staticmethod
    def _get_geo_coordinates(location):
        return location['geo_location']['coordinates']
