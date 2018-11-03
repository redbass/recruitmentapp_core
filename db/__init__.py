import gridfs
from pymongo import MongoClient
from pymongo.database import Database

from config import settings

DATABASE_NAME = 'recruitment_app'

_db = None
_fs = None


def get_db() -> Database:
    global _db

    if not _db:
        client = _get_mongo_client()
        db_name = get_db_name()
        _db = client[db_name]

    return _db


def get_grid_fs() -> gridfs.GridFS:
    global _fs

    if not _fs:
        db = get_db()
        _fs = gridfs.GridFS(db)

    return _fs


def get_db_name():

    db_name = settings.DATABASE_NAME or DATABASE_NAME

    if settings.DATABASE_DB_SUFFIX:
        db_name = db_name + '_' + settings.DATABASE_DB_SUFFIX

    return db_name


def _get_mongo_client() -> MongoClient:

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

    return MongoClient(url, **params)
