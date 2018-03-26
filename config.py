import os


class BaseConfig(object):
    DEBUG = False
    DEFAULT_PORT = None

    DATABASE_HOST = ''
    DATABASE_PORT = None
    DATABASE_USER = None
    DATABASE_PASSWORD = None
    DATABASE_DB_SUFFIX = ''


class StagingConfig(BaseConfig):
    DATABASE_HOST = 'ds229909.mlab.com'
    DATABASE_PORT = 299009
    DATABASE_USER = 'test'
    DATABASE_PASSWORD = 'test'
    DATABASE_DB_SUFFIX = ''


class DevConfig(StagingConfig):
    DEBUG = True
    DEFAULT_PORT = 5001

    DATABASE_HOST = 'localhost'
    DATABASE_PORT = 27017
    DATABASE_DB_SUFFIX = ''
    DATABASE_USER = None
    DATABASE_PASSWORD = None


class TestConfig(DevConfig):
    DATABASE_DB_SUFFIX = 'test'


def _get_settings():
    app_env = os.environ.get('APP_ENV')

    app_configs = {
        'test': TestConfig,
        'dev': DevConfig,
        'staging': StagingConfig
    }

    if app_env not in app_configs.keys():
        raise Exception('APP_ENV "{app_env}" not supported'.format(app_env=app_env))

    return app_configs.get(app_env)()


settings = _get_settings()
