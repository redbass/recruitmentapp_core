from flask.ext.login import LoginManager

from auth.user import User

_login_manager = None


def setup_login_manager(a):
    global _login_manager

    _login_manager = LoginManager()
    _login_manager.init_app(a)
    _login_manager.login_view = "login"

    @_login_manager.user_loader
    def load_user(user_id):
        return User(user_id)

    return _login_manager


def get_login_manager(a):
    global _login_manager

    if not _login_manager:
        raise Exception('Run setup_login_manager to initialize a login_manager')

    return _login_manager
