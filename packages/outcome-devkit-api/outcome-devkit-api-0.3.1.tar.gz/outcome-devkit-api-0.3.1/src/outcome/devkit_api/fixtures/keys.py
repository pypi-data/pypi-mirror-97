"""Public and private key fixtures."""

import warnings
from pathlib import Path

import jwt
import pytest
from outcome.utils import feature_set
from outcome.utils.config import Config

check_idp_key_feature = 'outcome.devkit_api.fixtures.keys.check_idp_keys'

feature_set.register_feature(check_idp_key_feature, default=True)


def _get_key(key: str):
    with open(Path(Path(__file__).parent, 'keys', key)) as file:
        return file.read()


@pytest.fixture(scope='session')
def private_key() -> str:
    return _get_key('private.key')


@pytest.fixture(scope='session')
def public_key() -> str:
    return _get_key('public.key')


@pytest.fixture(scope='session')
def incorrect_public_key() -> str:
    return _get_key('incorrect.public.key')


@pytest.fixture(scope='session')
def other_public_key(incorrect_public_key: str) -> str:
    return incorrect_public_key


# This is called key_config and not just config
# to avoid fixture recursion where future config depends
# on idp_public_key, but idp_public_key depends on config..
@pytest.fixture(scope='session')
def key_config():
    return Config()


@pytest.fixture(scope='session')
def idp_public_key(key_config: Config) -> str:
    key = key_config.get('IDP_PUBLIC_KEY', _get_key('public.key'))
    assert isinstance(key, str)
    return key


# This used to test public/private key mismatches
@pytest.fixture(scope='session')
def alt_idp_public_key() -> str:
    return _get_key('incorrect.public.key')


@pytest.fixture(scope='session')
def idp_private_key(key_config: Config) -> str:
    key = key_config.get('IDP_PRIVATE_KEY', _get_key('private.key'))
    assert isinstance(key, str)
    return key


@pytest.fixture(scope='session', autouse=True)
def idp_key_check(idp_public_key: str, idp_private_key: str):
    run_idp_key_check(idp_public_key, idp_private_key)


def run_idp_key_check(idp_public_key: str, idp_private_key: str):
    try:
        token = jwt.encode({}, idp_private_key, algorithm='RS256')
        jwt.decode(token, idp_public_key, verify=True, algorithms=['RS256'])
    except jwt.DecodeError:
        if feature_set.is_active(check_idp_key_feature):
            raise Exception('There is a problem with the IDP keys')
        else:
            warnings.warn('The IDP Keys do not seem to match - this may cause tests to fail')


__all__ = [
    'key_config',
    'idp_key_check',
    'idp_private_key',
    'alt_idp_public_key',
    'private_key',
    'public_key',
    'idp_public_key',
    'other_public_key',
    'incorrect_public_key',
]
