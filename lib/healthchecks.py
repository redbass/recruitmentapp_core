from healthcheck import HealthCheck

from db.collections import db


def mongo_health():
    try:
        db.client.server_info()
        return True, 'UP'
    except Exception as e:
        return False, str(e)


def set_health_check(app):
    health = HealthCheck(app, '/health')

    health.add_check(mongo_health)
