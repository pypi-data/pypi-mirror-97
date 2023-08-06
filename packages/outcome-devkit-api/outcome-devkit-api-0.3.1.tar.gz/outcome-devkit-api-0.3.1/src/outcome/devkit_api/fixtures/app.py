"""Base app fixtures."""

import pytest
from fastapi import FastAPI


def base_app_raw() -> FastAPI:
    return FastAPI(title='TestApp', version='0.1.0')


@pytest.fixture
def base_app():
    return base_app_raw()


__all__ = ['base_app', 'base_app_raw']
