"""An extension to the starlette test client, that actually runs the requests."""

import logging
import os
from typing import TYPE_CHECKING, Optional, Union
from unittest.mock import Mock

import requests
from fastapi import FastAPI
from fastapi.testclient import TestClient
from urllib3.util import Url, parse_url

if TYPE_CHECKING:  # pragma: no cover
    import requests.types as rtypes  # type: ignore
else:
    rtypes = Mock()  # noqa: WPS440


logger = logging.getLogger(__name__)


class NativeSessionClient(requests.Session):  # pragma: no cover
    def __init__(self, scheme: str, host: str, port: int) -> None:
        super().__init__()
        self.scheme = scheme
        self.host = host
        self.port = port

    # NOTE: The method below can trigger a type error in the editor, but not
    # in pyright - this is due to the type definitions in pyright being a couple of
    # days more up to date...
    def request(  # noqa: WPS211
        self,
        method: str,
        url: rtypes.URL,
        params: Optional[rtypes.Params] = None,
        data: Optional[rtypes.Data] = None,
        headers: Optional[rtypes.Headers] = None,
        cookies: Optional[rtypes.Cookies] = None,
        files: Optional[rtypes.Files] = None,
        auth: Optional[rtypes.Auth] = None,
        timeout: Optional[rtypes.Timeout] = None,
        allow_redirects: Optional[rtypes.AllowRedirects] = None,
        proxies: Optional[rtypes.Proxies] = None,
        hooks: Optional[rtypes.Hooks] = None,
        stream: Optional[rtypes.Stream] = None,
        verify: Optional[rtypes.Verify] = None,
        cert: Optional[rtypes.Cert] = None,
        json: Optional[rtypes.Json] = None,
    ) -> requests.Response:  # pragma: no cover
        # Convert the url to a manageable type
        if isinstance(url, bytes):
            url = url.decode('utf8')
        else:
            url = str(url)

        parsed_url: Url = parse_url(url)  # noqa: WPS236

        # If we don't have a scheme, let's rebuild the url
        if not parsed_url.scheme:
            url = Url(
                scheme=self.scheme,
                auth=auth,
                host=self.host,
                port=self.port,
                path=parsed_url.path,
                query=parsed_url.query,
                fragment=parsed_url.fragment,
            ).url

        return super().request(
            method,
            url,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            files=files,
            auth=auth,
            timeout=timeout,
            allow_redirects=allow_redirects,
            proxies=proxies,
            hooks=hooks,
            stream=stream,
            verify=verify,
            cert=cert,
            json=json,
        )


def get_test_client(app: FastAPI) -> Union[NativeSessionClient, TestClient]:  # pragma: no cover
    if os.environ.get('TEST_CLIENT_MODE', 'app') == 'native':
        scheme = os.environ.get('TEST_CLIENT_SCHEME', 'http')
        host = os.environ.get('TEST_CLIENT_HOST', 'localhost')

        env_app_port = os.environ.get('APP_PORT')
        env_port = os.environ.get('PORT')
        env_test_client_port = os.environ.get('TEST_CLIENT_PORT')

        port = env_test_client_port or env_port or env_app_port

        assert port

        logger.info('Using testclient in native mode with scheme=%s, host=%s, port=%s', scheme, host, port)  # noqa: WPS323

        return NativeSessionClient(scheme=scheme, host=host, port=int(port))

    logger.info('Using testclient in app mode')

    return TestClient(app, raise_server_exceptions=os.environ.get('TEST_CLIENT_RAISE_EXCEPTIONS', False) == '1')
