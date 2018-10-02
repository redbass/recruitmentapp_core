from api.routes.admin_routes import add_admin_routes
from api.routes.hm_routes import add_hiring_manager_routes
from api.routes.routes import add_service_routes


def add_routes(app):
    add_admin_routes(app)
    add_hiring_manager_routes(app)
    add_service_routes(app)
