import datetime
import typing

import requests.types as rtypes
from requests import auth, cookies, exceptions, hooks, status_codes, structures, utils
from requests.packages.urllib3 import exceptions as urllib3_exceptions
from requests.packages.urllib3 import fields, filepost, util

default_hooks = hooks.default_hooks
CaseInsensitiveDict = structures.CaseInsensitiveDict
HTTPBasicAuth = auth.HTTPBasicAuth
cookiejar_from_dict = cookies.cookiejar_from_dict
get_cookie_header = cookies.get_cookie_header
RequestField = fields.RequestField
encode_multipart_formdata = filepost.encode_multipart_formdata
parse_url = util.parse_url
DecodeError = urllib3_exceptions.DecodeError
ReadTimeoutError = urllib3_exceptions.ReadTimeoutError
ProtocolError = urllib3_exceptions.ProtocolError
LocationParseError = urllib3_exceptions.LocationParseError
HTTPError = exceptions.HTTPError
MissingSchema = exceptions.MissingSchema
InvalidURL = exceptions.InvalidURL
ChunkedEncodingError = exceptions.ChunkedEncodingError
ContentDecodingError = exceptions.ContentDecodingError
ConnectionError = exceptions.ConnectionError
StreamConsumedError = exceptions.StreamConsumedError
guess_filename = utils.guess_filename
get_auth_from_url = utils.get_auth_from_url
requote_uri = utils.requote_uri
stream_decode_response_unicode = utils.stream_decode_response_unicode
to_key_val_list = utils.to_key_val_list
parse_header_links = utils.parse_header_links
iter_slices = utils.iter_slices
guess_json_utf = utils.guess_json_utf
super_len = utils.super_len
to_native_string = utils.to_native_string
codes = status_codes.codes

REDIRECT_STATI: typing.Tuple[int, ...]
DEFAULT_REDIRECT_LIMIT: int
CONTENT_CHUNK_SIZE: int
ITER_CHUNK_SIZE: int

class RequestEncodingMixin:
    @property
    def path_url(self) -> str: ...

class RequestHooksMixin:
    def register_hook(self, event: str, hook: rtypes.Hook) -> None: ...
    def deregister_hook(self, event: str, hook: rtypes.Hook) -> bool: ...

class Request(RequestHooksMixin):
    hooks: rtypes.Hooks
    method: str
    url: rtypes.URL
    headers: rtypes.Headers
    files: rtypes.Files
    data: rtypes.Data
    json: typing.Optional[rtypes.Json]
    params: rtypes.Params
    auth: rtypes.Auth
    cookies: rtypes.Cookies
    def __init__(
        self,
        method: str = ...,
        url: rtypes.URL = ...,
        *,
        headers: typing.Optional[rtypes.Headers] = ...,
        files: typing.Optional[rtypes.Files] = ...,
        data: typing.Optional[rtypes.Data] = ...,
        params: typing.Optional[rtypes.Params] = ...,
        auth: typing.Optional[rtypes.Auth] = ...,
        cookies: typing.Optional[rtypes.Cookies] = ...,
        hooks: typing.Optional[rtypes.Hooks] = ...,
        json: typing.Optional[rtypes.Json] = ...,
    ) -> None: ...
    def prepare(self) -> PreparedRequest: ...

class PreparedRequest(RequestEncodingMixin, RequestHooksMixin):
    method: str
    url: str
    headers: rtypes.Headers
    body: rtypes.Body
    hooks: rtypes.Hooks
    def __init__(self) -> None: ...
    def prepare(
        self,
        method: str = ...,
        url: rtypes.URL = ...,
        *,
        headers: typing.Optional[rtypes.Headers] = ...,
        files: typing.Optional[rtypes.Files] = ...,
        data: typing.Optional[rtypes.Data] = ...,
        params: typing.Optional[rtypes.Params] = ...,
        auth: typing.Optional[rtypes.Auth] = ...,
        cookies: typing.Optional[rtypes.Cookies] = ...,
        hooks: typing.Optional[rtypes.Hooks] = ...,
        json: typing.Optional[rtypes.Json] = ...,
    ) -> None: ...
    def copy(self) -> PreparedRequest: ...
    def prepare_method(self, method: str) -> None: ...
    def prepare_url(self, url: str, params: typing.Optional[rtypes.Params]) -> None: ...
    def prepare_headers(self, headers: typing.Optional[rtypes.Headers]) -> None: ...
    def prepare_body(
        self, data: typing.Optional[rtypes.Data], files: typing.Optional[rtypes.Files], json: typing.Optional[rtypes.Json] = ...,
    ) -> None: ...
    def prepare_content_length(self, body: typing.Optional[rtypes.Body]) -> None: ...
    def prepare_auth(self, auth: typing.Optional[rtypes.Auth], url: rtypes.URL = ...) -> None: ...
    def prepare_cookies(self, cookies: typing.Optional[rtypes.Cookies]) -> None: ...
    def prepare_hooks(self, hooks: typing.Optional[rtypes.Hooks]) -> None: ...

class Response:
    __attrs__: typing.Any
    _content: typing.Optional[bytes]  # undocumented
    status_code: int
    headers: rtypes.Headers
    raw: object
    url: str
    encoding: str
    history: typing.List[Response]
    reason: str
    cookies: rtypes.Cookies
    elapsed: datetime.timedelta
    request: PreparedRequest
    def __init__(self) -> None: ...
    def __bool__(self) -> bool: ...
    def __nonzero__(self) -> bool: ...
    def __iter__(self) -> typing.Iterator[bytes]: ...
    def __enter__(self) -> Response: ...
    def __exit__(self, *args: object) -> None: ...
    @property
    def next(self) -> typing.Optional[PreparedRequest]: ...
    @property
    def ok(self) -> bool: ...
    @property
    def is_redirect(self) -> bool: ...
    @property
    def is_permanent_redirect(self) -> bool: ...
    @property
    def apparent_encoding(self) -> str: ...
    def iter_content(self, chunk_size: typing.Optional[int] = ..., decode_unicode: bool = ...) -> typing.Iterator[object]: ...
    def iter_lines(
        self,
        chunk_size: typing.Optional[int] = ...,
        decode_unicode: bool = ...,
        delimiter: typing.Optional[typing.Union[typing.Text, bytes]] = ...,
    ) -> typing.Iterator[object]: ...
    @property
    def content(self) -> bytes: ...
    @property
    def text(self) -> str: ...
    def json(self, **kwargs: object) -> object: ...
    @property
    def links(self) -> typing.Dict[typing.Any, typing.Any]: ...
    def raise_for_status(self) -> None: ...
    def close(self) -> None: ...
