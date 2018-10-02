from json import dumps

from httpretty import httpretty

from exceptions.service import ServiceError
from services.postcode import get_postcode, OPEN_POSTCODE_GET, SERVICE_NAME
from test import UnitTestCase


class TestGetPostcode(UnitTestCase):

    def setUp(self):
        httpretty.enable()
        self.test_postcode = "EH8_8HE"
        super().setUp()

    def tearDown(self):
        httpretty.reset()
        super().tearDown()

    def test_get_postcode(self):
        body = {"Test": "Data"}
        httpretty.register_uri(
            httpretty.GET,
            OPEN_POSTCODE_GET.format(postcode=self.test_postcode),
            body=dumps(body)
        )

        postcode = get_postcode(self.test_postcode)

        self.assertEqual(body, postcode)

    def test_get_postcode_exception(self):
        httpretty.register_uri(
            httpretty.GET,
            OPEN_POSTCODE_GET.format(postcode=self.test_postcode),
            status=500,
            body=""
        )

        with self.assertRaises(ServiceError) as e:
            get_postcode(self.test_postcode)
            self.assertEqual(e.service, SERVICE_NAME)

    def test_get_postcode_not_found(self):
        the_message = "the message"
        httpretty.register_uri(
            httpretty.GET,
            OPEN_POSTCODE_GET.format(postcode=self.test_postcode),
            status=404,
            body='{{"error": "{msg}"}}'.format(msg=the_message)
        )

        with self.assertRaises(ValueError) as e:
            get_postcode(self.test_postcode)
            self.assertEqual(str(e), the_message)
