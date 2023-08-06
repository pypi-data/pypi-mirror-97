"""Various tools to help with testing apis."""

import os
from typing import Any, Callable, Dict, Tuple, Union

import pytest
from fastapi import FastAPI
from fastapi.routing import APIRoute

RouteKey = Tuple[str, str]
RouteResponses = Dict[Union[int, str], Dict[str, Any]]
RouteResponseModels = Dict[RouteKey, RouteResponses]


def api_raises_uncaught_exceptions(fn: Union[Callable[..., object], type]):  # pragma: no cover
    # We rely on FastAPI/starlette to map uncaught API exceptions to HTTP 500s
    # When this mapping feature is turned off (typically for debugging purposes), some tests will fail
    # This decorator skips the test if the feature is deactivated
    mark = pytest.mark.skipif(os.environ.get('TEST_CLIENT_RAISE_EXCEPTIONS', '0') == '1', reason='Fails in debug mode')
    return mark(fn)


def response_models_for_app(app: FastAPI) -> RouteResponseModels:  # pragma: no cover
    api_routes = (r for r in app.routes if isinstance(r, APIRoute))
    return {(r.name, r.path): r.responses for r in api_routes}
