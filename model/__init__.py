from uuid import uuid4


NOT_PROVIDED = "_NOT_PROVIDED_"


def create_id():
    return uuid4().hex
