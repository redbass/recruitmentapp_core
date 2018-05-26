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


def validate_period(period):

    if not period or type(period) != dict:
        raise ValueError("The given period is not a dict or is  null")

    if not isinstance(period.get('start'), datetime):
        raise ValueError("Start period have to be a valid date")

    if period.get('end') and not isinstance(period.get('end'), datetime):
        raise ValueError("End period have to be null or a valid date")
