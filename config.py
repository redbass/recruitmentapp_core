import os

from lib.base_config import BaseConfig


class ProductionConfig(BaseConfig):
    ENC_SEED = 'Erw9IfxRokPG2CKe'

    DATABASE_PORT = 21003
    DATABASE_USER = 'staging_recruitment_app'
    DATABASE_NAME = 'heroku_x8bftx89'


class StagingConfig(BaseConfig):
    ENC_SEED = 'Erw9IfxRokPG2CKe'

    DATABASE_PORT = 21003
    DATABASE_USER = 'staging_recruitment_app'
    DATABASE_NAME = 'heroku_x8bftx89'


class DevConfig(BaseConfig):
    ENC_SEED = 'G2kPfCexw9IRKEro'

    DATABASE_PORT = 29909
    DATABASE_USER = 'dev_recruitment_app'
    DATABASE_NAME = 'heroku_3kh06v65'


class LocalConfig(BaseConfig):
    DEBUG_MODE = True

    DATABASE_PORT = 27017


class TestConfig(LocalConfig):
    LOGIN_REQUIRED = True
    API_TOKEN_REQUIRED = True
    TEST_MODE = True
    DATABASE_DB_SUFFIX = 'test'


class TestCIConfig(TestConfig):
    DATABASE_DB_SUFFIX = 'test'


def _get_settings():
    app_env = os.environ.get('APP_ENV')

    app_configs = {
        'test': TestConfig,
        'test_ci': TestCIConfig,
        'local': LocalConfig,
        'dev': DevConfig,
        'staging': StagingConfig,
        'production': ProductionConfig
    }

    if app_env not in app_configs.keys():
        raise Exception(
            'APP_ENV "{app_env}" not supported'.format(app_env=app_env))

    return app_configs.get(app_env)()


settings = _get_settings()
