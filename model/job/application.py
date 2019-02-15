from db.collections import applications


def apply_advert(advert_id, candidate_id, email, first_name, last_name,
                 phone_number, metadata):
    candidate = {
        'candidate_id': candidate_id,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'phone_number': phone_number,
        'metadata': metadata
    }
    applications.update_one(
        {'_id': advert_id},
        {'$push': {
            'candidates': candidate
        }},
        upsert=True
    )


def get_advert_applications(advert_id):
    return applications.find_one({'_id': advert_id})
