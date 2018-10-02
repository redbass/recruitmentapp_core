from pymongo import MongoClient
from pymongo.database import Database

from config import settings

DATABASE_NAME = 'recruitment_app'


def get_client() -> MongoClient:

    url = 'mongodb://{host}:{port}/{db_name}'.format(
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT,
        db_name=get_db_name()
    )

    params = {
        'username': settings.DATABASE_USER,
        'password': settings.DATABASE_PASSWORD,
        'connectTimeoutMS': 10000,
        'socketTimeoutMS': 10000,
        'serverSelectionTimeoutMS': 10000
    }

    client = MongoClient(url, **params)
    return client


def get_db() -> Database:
    client = get_client()

    db_name = get_db_name()

    return client[db_name]


def get_db_name():

    db_name = settings.DATABASE_NAME or DATABASE_NAME

    if settings.DATABASE_DB_SUFFIX:
        db_name = db_name + '_' + settings.DATABASE_DB_SUFFIX

    return db_name
