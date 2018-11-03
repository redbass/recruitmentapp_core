from model.job.job_advert import \
    pay_job_advert as pay_advert


def pay_job_advert(advert_id, job_id):
    return pay_advert(advert_id=advert_id, job_id=job_id)
