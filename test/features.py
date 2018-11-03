

def crate_stripe_charge_response(job_id=None,
                                 advert_id=None,
                                 company_id=None):
    job_id = job_id or '8318baba5c22402da9755986953702b0'
    advert_id = advert_id or 'ea670554ea18428789ac6db30d07a755'
    company_id = company_id or 'hm@company.com'
    return {
        'id': 'evt_1DPxSQGS8uFqrEEaybIMuG06',
        'object': 'event',
        'data': {
            'object': {
                'id': 'ch_1DPxSPGS8uFqrEEa55JS3QQj',
                'amount': 2000,
                'metadata': {
                    'job_id': job_id,
                    'advert_id': advert_id
                },
                'source': {
                    'name': company_id,
                }
            }
        },
        'type': 'charge.succeeded'
    }
