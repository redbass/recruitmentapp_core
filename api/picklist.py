from api.handler import json_response
from auth.api_token import api_token_required


@json_response
@api_token_required
def picklist(name):

    return {
        "roletitles": [
            {
                "id": "software-engineer",
                "title": "Software Engineer"
            },
            {
                "id": "qa-engineer",
                "title": "QA Engineer"
            }
        ],
        "rate": [
            {
                "id": "0-150",
                "title": "£0-£150"
            },
            {
                "id": "150-250",
                "title": "£150-£250"
            }
        ],
        "locations": [
            {
                "id": "bath",
                "title": "Bath"
            },
            {
                "id": "bristol",
                "title": "Bristol"
            },
            {
                "id": "cardiff",
                "title": "Cardiff"
            }
        ]
    }.get(name, [])
