from typing import IO, Any, Callable, Iterable, List, Mapping, MutableMapping, Optional, Text, Tuple, Union

from requests import auth, cookies, models

RequestsCookieJar = cookies.RequestsCookieJar
Request = models.Request
Response = models.Response
PreparedRequest = models.PreparedRequest

Hook = Callable[[Response], Any]
_Hooks = MutableMapping[Text, List[Hook]]
_HooksInput = MutableMapping[Text, Union[Iterable[Hook], Hook]]

Body = Union[bytes, Text]

URL = Union[str, bytes, Text]
Params = Union[bytes, MutableMapping[Text, Text]]
Data = Union[Text, bytes, Mapping[str, Any], Mapping[Text, Any], Iterable[Tuple[Text, Optional[Text]]], IO]
Headers = MutableMapping[Text, Text]
Cookies = Union[RequestsCookieJar, MutableMapping[Text, Text]]
Files = MutableMapping[Text, IO[Any]]
Auth = Union[Tuple[Text, Text], auth.AuthBase, Callable[[PreparedRequest], PreparedRequest]]
Timeout = Union[float, Tuple[float, float], Tuple[float, None]]
AllowRedirects = bool
Proxies = MutableMapping[Text, Text]
Hooks = _HooksInput
Stream = bool
Verify = Union[bool, Text]
Cert = Union[Text, Tuple[Text, Text]]
Json = Any
