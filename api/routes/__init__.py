from api.routes.routes import add_public_routes
from api.routes.admin_routes import add_admin_routes


def add_routes(app):
    add_admin_routes(app)
    add_public_routes(app)
