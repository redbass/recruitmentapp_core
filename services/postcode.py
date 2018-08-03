import requests

from exceptions.service import ServiceError

SERVICE_NAME = "Postcode.io"
OPEN_POSTCODE_API_ROOT = "http://api.postcodes.io/"
OPEN_POSTCODE_GET = OPEN_POSTCODE_API_ROOT + "postcodes/{postcode}"


def get_postcode(postcode):

    url = OPEN_POSTCODE_API_ROOT + "postcodes/" + postcode
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        raise ValueError(response.json().get('error'))

    raise ServiceError(SERVICE_NAME)
