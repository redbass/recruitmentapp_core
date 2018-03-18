from api.job import get_jobs


def add_routes(app):
    app.add_url_rule('/api/job/', 'get_jobs', get_jobs, methods=['GET'])
