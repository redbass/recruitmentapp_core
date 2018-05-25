from datetime import datetime


def create_period(start: datetime = None,
                  end: datetime = None):
    return {
        'start': start or datetime.utcnow(),
        'end': end
    }


def create_duration():

    return {
        'dates': create_period(None, None),
        'fix_period': None
    }
