from typing import TYPE_CHECKING, Any, Awaitable, Callable, Optional, Sequence, Union

import requests
import requests.auth
import requests.cookies
from starlette.types import Receive, Scope, Send

ASGIInstance = Callable[[Receive, Send], Awaitable[None]]
ASGI2App = Callable[[Scope], ASGIInstance]
ASGI3App = Callable[[Scope, Receive, Send], Awaitable[None]]

if TYPE_CHECKING:
    import requests.types as rtypes

class TestClient(requests.Session):
    def __init__(
        self, app: Union[ASGI2App, ASGI3App], base_url: str = ..., raise_server_exceptions: bool = ..., root_path: str = ...,
    ) -> None: ...
    def request(
        self,
        method: str = ...,
        url: rtypes.URL = ...,
        *,
        headers: Optional[rtypes.Headers] = ...,
        files: Optional[rtypes.Files] = ...,
        data: Optional[rtypes.Data] = ...,
        params: Optional[rtypes.Params] = ...,
        auth: Optional[rtypes.Auth] = ...,
        cookies: Optional[rtypes.Cookies] = ...,
        hooks: Optional[rtypes.Hooks] = ...,
        json: Optional[rtypes.Json] = ...,
        timeout: Optional[rtypes.Timeout] = ...,
        allow_redirects: Optional[rtypes.AllowRedirects] = ...,
        proxies: Optional[rtypes.Proxies] = ...,
        stream: Optional[rtypes.Stream] = ...,
        verify: Optional[rtypes.Verify] = ...,
        cert: Optional[rtypes.Cert] = ...,
    ) -> requests.Response: ...
    def get(
        self,
        url: rtypes.URL = ...,
        *,
        headers: Optional[rtypes.Headers] = ...,
        params: Optional[rtypes.Params] = ...,
        auth: Optional[rtypes.Auth] = ...,
        cookies: Optional[rtypes.Cookies] = ...,
        hooks: Optional[rtypes.Hooks] = ...,
        timeout: Optional[rtypes.Timeout] = ...,
        allow_redirects: Optional[rtypes.AllowRedirects] = ...,
        proxies: Optional[rtypes.Proxies] = ...,
        stream: Optional[rtypes.Stream] = ...,
        verify: Optional[rtypes.Verify] = ...,
        cert: Optional[rtypes.Cert] = ...,
    ) -> requests.Response: ...
    def options(
        self,
        url: rtypes.URL = ...,
        *,
        headers: Optional[rtypes.Headers] = ...,
        params: Optional[rtypes.Params] = ...,
        auth: Optional[rtypes.Auth] = ...,
        cookies: Optional[rtypes.Cookies] = ...,
        hooks: Optional[rtypes.Hooks] = ...,
        timeout: Optional[rtypes.Timeout] = ...,
        allow_redirects: Optional[rtypes.AllowRedirects] = ...,
        proxies: Optional[rtypes.Proxies] = ...,
        stream: Optional[rtypes.Stream] = ...,
        verify: Optional[rtypes.Verify] = ...,
        cert: Optional[rtypes.Cert] = ...,
    ) -> requests.Response: ...
    def head(
        self,
        url: rtypes.URL = ...,
        *,
        headers: Optional[rtypes.Headers] = ...,
        params: Optional[rtypes.Params] = ...,
        auth: Optional[rtypes.Auth] = ...,
        cookies: Optional[rtypes.Cookies] = ...,
        hooks: Optional[rtypes.Hooks] = ...,
        timeout: Optional[rtypes.Timeout] = ...,
        allow_redirects: Optional[rtypes.AllowRedirects] = ...,
        proxies: Optional[rtypes.Proxies] = ...,
        stream: Optional[rtypes.Stream] = ...,
        verify: Optional[rtypes.Verify] = ...,
        cert: Optional[rtypes.Cert] = ...,
    ) -> requests.Response: ...
    def delete(
        self,
        url: rtypes.URL = ...,
        *,
        headers: Optional[rtypes.Headers] = ...,
        params: Optional[rtypes.Params] = ...,
        auth: Optional[rtypes.Auth] = ...,
        cookies: Optional[rtypes.Cookies] = ...,
        hooks: Optional[rtypes.Hooks] = ...,
        timeout: Optional[rtypes.Timeout] = ...,
        allow_redirects: Optional[rtypes.AllowRedirects] = ...,
        proxies: Optional[rtypes.Proxies] = ...,
        stream: Optional[rtypes.Stream] = ...,
        verify: Optional[rtypes.Verify] = ...,
        cert: Optional[rtypes.Cert] = ...,
    ) -> requests.Response: ...
    def post(
        self,
        url: rtypes.URL = ...,
        *,
        headers: Optional[rtypes.Headers] = ...,
        files: Optional[rtypes.Files] = ...,
        data: Optional[rtypes.Data] = ...,
        params: Optional[rtypes.Params] = ...,
        auth: Optional[rtypes.Auth] = ...,
        cookies: Optional[rtypes.Cookies] = ...,
        hooks: Optional[rtypes.Hooks] = ...,
        json: Optional[rtypes.Json] = ...,
        timeout: Optional[rtypes.Timeout] = ...,
        allow_redirects: Optional[rtypes.AllowRedirects] = ...,
        proxies: Optional[rtypes.Proxies] = ...,
        stream: Optional[rtypes.Stream] = ...,
        verify: Optional[rtypes.Verify] = ...,
        cert: Optional[rtypes.Cert] = ...,
    ) -> requests.Response: ...
    def put(
        self,
        url: rtypes.URL = ...,
        *,
        headers: Optional[rtypes.Headers] = ...,
        files: Optional[rtypes.Files] = ...,
        data: Optional[rtypes.Data] = ...,
        params: Optional[rtypes.Params] = ...,
        auth: Optional[rtypes.Auth] = ...,
        cookies: Optional[rtypes.Cookies] = ...,
        hooks: Optional[rtypes.Hooks] = ...,
        json: Optional[rtypes.Json] = ...,
        timeout: Optional[rtypes.Timeout] = ...,
        allow_redirects: Optional[rtypes.AllowRedirects] = ...,
        proxies: Optional[rtypes.Proxies] = ...,
        stream: Optional[rtypes.Stream] = ...,
        verify: Optional[rtypes.Verify] = ...,
        cert: Optional[rtypes.Cert] = ...,
    ) -> requests.Response: ...
    def patch(
        self,
        url: rtypes.URL = ...,
        *,
        headers: Optional[rtypes.Headers] = ...,
        files: Optional[rtypes.Files] = ...,
        data: Optional[rtypes.Data] = ...,
        params: Optional[rtypes.Params] = ...,
        auth: Optional[rtypes.Auth] = ...,
        cookies: Optional[rtypes.Cookies] = ...,
        hooks: Optional[rtypes.Hooks] = ...,
        json: Optional[rtypes.Json] = ...,
        timeout: Optional[rtypes.Timeout] = ...,
        allow_redirects: Optional[rtypes.AllowRedirects] = ...,
        proxies: Optional[rtypes.Proxies] = ...,
        stream: Optional[rtypes.Stream] = ...,
        verify: Optional[rtypes.Verify] = ...,
        cert: Optional[rtypes.Cert] = ...,
    ) -> requests.Response: ...
    def websocket_connect(self, url: str, subprotocols: Optional[Sequence[str]] = ..., **kwargs: object) -> Any: ...
    def __enter__(self) -> "TestClient": ...
    def __exit__(self, *args: object) -> None: ...
    async def lifespan(self) -> None: ...
    async def wait_startup(self) -> None: ...
    async def wait_shutdown(self) -> None: ...
