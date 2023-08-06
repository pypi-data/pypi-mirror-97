"""A fixture for the config object."""

import pytest
from outcome.devkit_api.fixtures.keys import *  # type: ignore  # noqa: F403,WPS347,F401
from outcome.utils.config import Config


@pytest.fixture(scope='session')
def app_config() -> Config:
    return Config(
        defaults={
            'DB_DATABASE': 'postgres',
            'DB_USERNAME': 'postgres',
            'DB_PASSWORD': 'postgres',
            'DB_SERVER': '127.0.0.1',
            'DB_PORT': '5432',
            'APP_NAME': 'apikit',
            'APP_VERSION': '0.1.0',
        },
    )


@pytest.fixture(scope='session')
def config(app_config: Config, idp_public_key: str, private_key: str, public_key: str) -> Config:
    app_config.default_backend.defaults = {
        **app_config.default_backend.defaults,
        'APP_PUBLIC_KEY': public_key,
        'APP_PRIVATE_KEY': private_key,
        'IDP_PUBLIC_KEY': idp_public_key,
    }
    return app_config


__all__ = ['config']
