from flask import Flask

from api.route import add_routes
from auth.jwt import setup_jwt
from config import settings
from lib.healthchecks import set_health_check

_app = None


def get_app(*args, **kwarg) -> Flask:

    global _app

    if not _app:
        _app = Flask(__name__, *args, **kwarg)
        _app.config.update(
            SECRET_KEY='secret_xxx'  # TODO: SET REAL ONE
        )

        setup_jwt(_app)
        add_routes(_app)
        set_health_check(_app)

    return _app


if __name__ == '__main__':
    get_app().run(debug=settings.DEBUG_MODE, port=settings.DEFAULT_PORT)
