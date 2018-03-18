from os import environ


class Config:
    TEST_MODE = True

    DATABASE = {
        'url': 'localhost',
        'port': 27017,
    }


class TestConfig(Config):
    TEST_MODE = False


def get_config():
    if _is_in_debug_mode():
        return TestConfig
    return Config


def _is_in_debug_mode():
    return environ.get('TEST_MODE', False)
