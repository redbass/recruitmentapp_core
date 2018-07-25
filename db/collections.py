from pymongo import TEXT

from db import get_db

db = get_db()
jobs = db.jobs
users = db.users
companies = db.companies


# Indexes
def create_indexes():
    _create_text_index()


def _create_text_index():
    jobs.create_index(
        [('title', TEXT), ('description', TEXT)], name='search_index')


create_indexes()
