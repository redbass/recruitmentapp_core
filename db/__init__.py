from pymongo import MongoClient
from pymongo.database import Database

from config import settings

DATABASE_NAME = 'recruitment_app'


def get_client() -> MongoClient:
    params = {
        'host': settings.DATABASE_HOST,
        'port': settings.DATABASE_PORT,
        'username': settings.DATABASE_USER,
        'password': settings.DATABASE_PASSWORD,
    }

    return MongoClient(**params)


def get_db() -> Database:
    client = get_client()

    db_name = DATABASE_NAME + '_' + settings.DATABASE_DB_SUFFIX

    return client[db_name]
