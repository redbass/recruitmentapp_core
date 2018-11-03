from db.collections import payments


def store_payment(request_content):
    response_object = request_content['data']['object']

    payment_id = response_object['id']
    job_id = response_object['metadata']['job_id']
    advert_id = response_object['metadata']['advert_id']

    payments.insert_one({
        '_id': payment_id,
        'content': request_content
    })

    return payment_id, job_id, advert_id
