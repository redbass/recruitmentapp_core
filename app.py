from flask import Flask

from api import set_flask_json_encoder
from api.routes import add_routes
from auth.jwt import setup_jwt
from config import settings
from lib.healthchecks import set_health_check

__app__ = None


def get_app(*args, **kwarg) -> Flask:

    global __app__

    if not __app__:
        __app__ = Flask(__name__, *args, **kwarg)
        __app__.config.update(
            SECRET_KEY=settings.FLASK_SECRET_KEY,
            MAX_CONTENT_LENGTH=settings.MAX_CONTENT_LENGTH
        )

        setup_jwt(__app__)
        add_routes(__app__)
        set_health_check(__app__)
        set_flask_json_encoder(__app__)

    return __app__


if __name__ == '__main__':
    get_app().run(debug=settings.DEBUG_MODE, port=settings.DEFAULT_PORT)
