from db.collections import applications
from model.job.job import get_job


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


def get_advert_applications_by_job_id(job_id):

    job = get_job(job_id=job_id)
    adverts_ids = [ad['_id'] for ad in job['adverts']]

    candidates = []
    for advert_id in adverts_ids:
        ad_applic = get_advert_applications(advert_id)
        candidates += ad_applic['candidates'] if ad_applic else []

    return {'candidates': candidates}
