from api.handler import json_response


@json_response
def picklist(name):
    picklists = {
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
    }

    return picklists.get(name, [])
