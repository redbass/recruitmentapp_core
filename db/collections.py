from pymongo import TEXT, ASCENDING

from db import get_db

db = get_db()
jobs = db.jobs
users = db.users
companies = db.companies
payments = db.payments
files = db['fs.files']

# Indexes
SEARCH_INDEX_NAME = 'search_index'
TTL_FILES_NAME = 'files_ttl'


def setup_database():
    _create_text_index()
    _set_ttl_files()


def _set_ttl_files():
    if TTL_FILES_NAME not in files.index_information():
        files.create_index(
            [('uploadDate', ASCENDING)], expireAfterSeconds=15780000,
            name=TTL_FILES_NAME)


def _create_text_index():
    if SEARCH_INDEX_NAME not in jobs.index_information():
        jobs.create_index(
            [('title', TEXT), ('description', TEXT)], name=SEARCH_INDEX_NAME)


setup_database()
