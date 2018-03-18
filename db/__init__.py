from pymongo import MongoClient
from pymongo.database import Database

from config import get_config

DATABASE_NAME = 'recruitment_app'


def get_client() -> MongoClient:
    config = get_config()
    return MongoClient(config.DATABASE['url'],
                       config.DATABASE['port'])


def get_db() -> Database:
    config = get_config()
    client = get_client()

    db_name = DATABASE_NAME
    if config.TEST_MODE:
        db_name += '_test'

    return client[db_name]
