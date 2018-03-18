from api.handler import json_response


@json_response
def get_jobs():
    return {
        'test': 'rresv;lsfla sdlasd'
    }
