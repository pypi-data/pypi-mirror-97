__all__ = (
    'PararamioException',
    'PararamioRequestException',
    'PararamioMethodNotAllowed',
    'PararamioXSFRRequestError',
    'PararamioServerResponseException',
    'PararamioAuthenticationException',
    'PararamioValidationException',
    'PararamioHTTPRequestException',
    'PararamioLimitExceededException',
)

import json
from json import JSONDecodeError
from typing import IO, List, Optional, Union
from urllib.error import HTTPError


class PararamioException(Exception):
    pass


class PararamioValidationException(PararamioException):
    pass


class PararamioHTTPRequestException(HTTPError, PararamioException):
    _response: Union[bytes, None]
    fp: Optional[IO[bytes]]

    def __init__(self, url: str, code: int, msg: str, hdrs: List, fp: IO[bytes]):
        self.fp = None
        self._response = None
        super().__init__(url, code, msg, hdrs, fp)

    @property
    def response(self):
        if not self._response and self.fp is not None:
            self._response = self.fp.read()
        return self._response

    @property
    def message(self) -> Union[str, None]:
        if self.code in [403, 400]:
            try:
                return json.loads(self.response).get('message', {})
            except JSONDecodeError:
                pass
        return None


class PararamioRequestException(PararamioException):
    pass


class PararamioServerResponseException(PararamioRequestException):
    response: dict

    def __init__(self, msg: str, response: dict):
        self.msg = msg
        self.response = response

    def __str__(self):
        return f'{self.__class__.__name__}, {self.msg or " has been raised"}'


class PararamioLimitExceededException(PararamioRequestException):
    pass


class PararamioMethodNotAllowed(PararamioException):
    pass


class PararamioAuthenticationException(PararamioException):
    pass


class PararamioXSFRRequestError(PararamioAuthenticationException):
    pass
