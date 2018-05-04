from unittest import TestCase

from model.location import Location


class TestLocation(TestCase):

    def test_location(self):
        lat = 10.0001001001
        lng = 11.1010001001
        point = Location(lng, lat)

        self.assertEqual(point.longitude, lng)
        self.assertEqual(point.latitude, lat)

    def test_location_longitude_validity(self):

        valid_longitude = [-180, -90.1234, 0, 99.3333, 180]
        invalid_longitude = [-270, -181, -180.00000001, 180.0000001, 181, 270]

        for lng in valid_longitude:
            location = Location(lng, 0)
            self.assertEqual(location.longitude, lng)

        for lng in invalid_longitude:
            with self.assertRaises(ValueError):
                Location(lng, 0)

    def test_location_latitude_validity(self):

        valid_latitudes = [-90, -45.1234, 0, 33.3333, 90]
        invalid_latitudes = [-180, -91, -90.0000000001, 90.000000001, 91, 180]

        for lat in valid_latitudes:
            location = Location(0, lat)
            self.assertEqual(location.latitude, lat)

        for lat in invalid_latitudes:
            with self.assertRaises(ValueError):
                Location(0, lat)

    def test_location_is_geo_json_point(self):
        lat = 10.0001001001
        lng = 11.1010001001
        point = Location(lng, lat)

        expected_geo_json_point = {
            'type': "Point",
            'coordinates': [lng, lat]
        }

        result = point.get_geo_json_point()

        self.assertEqual(expected_geo_json_point, result)
