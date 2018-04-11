import os

from lib.base_config import BaseConfig


class StagingConfig(BaseConfig):
    ENC_SEED = 'G2kPfCexw9IRKEro'

    DATABASE_HOST = 'ds229909.mlab.com'
    DATABASE_PORT = 299009
    DATABASE_USER = 'dev_recruitment_app'
    DATABASE_DB_SUFFIX = ''
    DATABASE_PASSWORD = '076970ce739732354c51bae004fd9f9b'


class DevConfig(StagingConfig):
    DEBUG_MODE = True
    DEFAULT_PORT = 5001

    DATABASE_HOST = 'localhost'
    DATABASE_PORT = 27017
    DATABASE_DB_SUFFIX = ''
    DATABASE_USER = None
    DATABASE_PASSWORD = None


class TestConfig(DevConfig):
    LOGIN_REQUIRED = False
    TEST_MODE = True
    DATABASE_DB_SUFFIX = 'test'


class TestCIConfig(TestConfig):
    DATABASE_DB_SUFFIX = 'test'


def _get_settings():
    app_env = os.environ.get('APP_ENV')

    app_configs = {
        'test': TestConfig,
        'test_ci': TestCIConfig,
        'dev': DevConfig,
        'staging': StagingConfig
    }

    if app_env not in app_configs.keys():
        raise Exception(
            'APP_ENV "{app_env}" not supported'.format(app_env=app_env))

    return app_configs.get(app_env)()


settings = _get_settings()
