from db.collections import picklist


ALLOWED_PICKLIST_NAMES = ['duration']


def store_piclikst(picklist_type, picklist_values):

    if picklist_type not in ALLOWED_PICKLIST_NAMES:
        raise ValueError("Invalid picklist name")

    _validate_picklist_values(picklist_values)

    picklist.update_one({'_id': picklist_type},
                        {'$set': {'values': picklist_values}},
                        upsert=True)


def get_picklist(picklist_type):
    stored = picklist.find_one({'_id': picklist_type})
    return stored.get('values') if stored else None


def _validate_picklist_values(picklist_values):

    if not isinstance(picklist_values, list) or len(picklist_values) == 0:
        raise ValueError("Picklist value has to be pair of key and value")

    for value in picklist_values:
        if 'key' not in value or 'value' not in value:
            raise ValueError("Picklist value has to be pair of key and value")
