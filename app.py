from flask import Flask

from api.route import add_routes, add_test_routes
from auth import setup_login_manager

__recruitment_app__ = None


def get_app() -> Flask:
    global __recruitment_app__

    if not __recruitment_app__:
        __recruitment_app__ = Flask(__name__)
    return __recruitment_app__


def run_app():
    app = get_app()
    app.config.update(
        SECRET_KEY='secret_xxx'  # TODO: SET REAL ONE
    )
    setup_login_manager(app)
    add_routes(app)
    add_test_routes(app)  # TODO: remove

    app.run(debug=True)


if __name__ == '__main__':
    run_app()
