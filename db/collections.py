from pymongo import TEXT

from db import get_db

db = get_db()
jobs = db.jobs
users = db.users
companies = db.companies

# Indexes
SEARCH_INDEX_NAME = 'search_index'


def create_indexes():
    _create_text_index()


def _create_text_index():
    if SEARCH_INDEX_NAME not in jobs.index_information():
        jobs.create_index(
            [('title', TEXT), ('description', TEXT)], name=SEARCH_INDEX_NAME)


create_indexes()
