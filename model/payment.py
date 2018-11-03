from db.collections import payments


def store_payment(payment_id, payment_content):
    payments.insert_one({
        '_id': payment_id,
        'content': payment_content
    })
