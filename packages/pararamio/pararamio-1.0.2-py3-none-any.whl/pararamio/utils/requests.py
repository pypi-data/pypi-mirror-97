import codecs
import json
import logging
import mimetypes
import os
from http.client import HTTPResponse
from io import BytesIO
from typing import BinaryIO, List, Optional, Tuple, Union
from urllib.error import HTTPError
from urllib.request import HTTPCookieProcessor, Request, build_opener

from pararamio._types import CookieJarT, HeaderLikeT
from pararamio.constants import BASE_API_URL, FILE_UPLOAD_URL, REQUEST_TIMEOUT as TIMEOUT, UPLOAD_TIMEOUT, VERSION
from pararamio.exceptions import PararamioHTTPRequestException


__all__ = ('api_request', 'bot_request', 'upload_file', 'xupload_file', 'delete_file', 'download_file', 'raw_api_request')
log = logging.getLogger('pararamio')
UA_HEADER = f'pararamio lib version {VERSION}'
DEFAULT_HEADERS = {
    'Content-type': 'application/json',
    'Accept':       'application/json',
    'User-agent':   UA_HEADER
}
writer = codecs.lookup('utf-8')[3]


def multipart_encode(fd: BinaryIO,
                     fields: List[Tuple[str, Union[str, None, int]]] = None,
                     boundary: str = None,
                     form_field_name: str = 'data',
                     filename: str = None,
                     content_type: str = None) -> bytes:
    if fields is None:
        fields = []
    if boundary is None:
        boundary = 'FORM-BOUNDARY'
    body = BytesIO()

    def write(text: str):
        nonlocal body
        writer(body).write(text)

    if fields:
        for (key, value) in fields:
            if value is None:
                continue
            write(f'--{boundary}\r\n')
            write(f'Content-Disposition: form-data; name="{key}"')
            write(f'\r\n\r\n{value}\r\n')
    if not filename:
        filename = os.path.basename(fd.name)
    if not content_type:
        content_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
    fd.seek(0)
    write(f'--{boundary}\r\n')
    write(f'Content-Disposition: form-data; name="{form_field_name}"; filename="{filename}"\r\n')
    write(f'Content-Type: {content_type}\r\n\r\n')
    body.write(fd.read())
    write(f'\r\n--{boundary}--\r\n\r\n')
    return body.getvalue()


def bot_request(url: str, key: str, method: str = 'GET', data: Optional[dict] = None, headers: dict = None, timeout: int = TIMEOUT):
    _headers = {'X-APIToken': key, **DEFAULT_HEADERS}
    if headers:
        _headers = {**_headers, **headers}
    return api_request(url=url, method=method, data=data, headers=_headers, timeout=timeout)


def _base_request(url: str, method: str = 'GET', data: bytes = None, headers: dict = None, cookie_jar: CookieJarT = None,
                  timeout: int = TIMEOUT) -> HTTPResponse:
    _url = f'{BASE_API_URL}{url}'
    _headers = DEFAULT_HEADERS
    if headers:
        _headers = {**_headers, **headers}
    opener = build_opener(*[HTTPCookieProcessor(cookie_jar)] if cookie_jar is not None else [])
    _data = None
    if data:
        _data = data
    rq = Request(_url, _data, method=method, headers=_headers)
    log.debug('%s - %s - %s - %s - %s', _url, method, data, headers, cookie_jar)
    try:
        return opener.open(rq, timeout=timeout)
    except HTTPError as e:
        log.error('%s - %s - %s', _url, method, e)
        # noinspection PyUnresolvedReferences
        raise PararamioHTTPRequestException(e.filename, e.code, e.msg, e.hdrs, e.fp)  # type: ignore[attr-defined]


def _base_file_request(url: str, method='GET', data: bytes = None, headers: Optional[HeaderLikeT] = None, cookie_jar: CookieJarT = None,  # type: ignore
                       timeout: int = TIMEOUT) -> BytesIO:
    _url = f'{FILE_UPLOAD_URL}{url}'
    opener = build_opener(HTTPCookieProcessor(cookie_jar))
    if not headers:
        headers = {}
    rq = Request(_url, data, method=method, headers=headers)
    log.debug('%s - %s - %s - %s - %s', url, method, data, headers, cookie_jar)
    try:
        resp = opener.open(rq, timeout=timeout)
        if 200 >= resp.getcode() < 300:
            return resp
    except HTTPError as e:
        log.error('%s - %s - %s', _url, method, e)
        # noinspection PyUnresolvedReferences
        raise PararamioHTTPRequestException(e.filename, e.code, e.msg, e.hdrs, e.fp)  # type: ignore[attr-defined]


def upload_file(fp: BinaryIO,
                perm: str,
                filename: str = None,
                file_type=None,
                headers: HeaderLikeT = None,
                cookie_jar: CookieJarT = None,
                timeout: int = UPLOAD_TIMEOUT):
    url = f'/upload/{perm}'
    boundary = 'FORM-BOUNDARY'
    _headers = {
        'User-agent':   UA_HEADER,
        **(headers or {}),
        'Accept':       'application/json',
        'Content-Type': f'multipart/form-data; boundary={boundary}'
    }
    data = multipart_encode(fp, boundary=boundary, form_field_name='file', filename=filename, content_type=file_type)
    resp = _base_file_request(url, method='POST', data=data, headers=_headers, cookie_jar=cookie_jar, timeout=timeout)
    return json.loads(resp.read())


def xupload_file(fp: BinaryIO, fields: List[Tuple[str, Union[str, None, int]]], headers: HeaderLikeT = None, cookie_jar: CookieJarT = None,
                 timeout: int = UPLOAD_TIMEOUT) -> dict:
    url = '/xupload'
    boundary = 'FORM-BOUNDARY'
    _headers = {
        'User-agent':   UA_HEADER,
        **(headers or {}),
        'Accept':       'application/json',
        'Content-Type': f'multipart/form-data; boundary={boundary}'
    }
    data = multipart_encode(fp, fields, boundary=boundary)
    resp = _base_file_request(url, method='POST', data=data, headers=_headers, cookie_jar=cookie_jar, timeout=timeout)
    return json.loads(resp.read())


def delete_file(guid: str, headers: HeaderLikeT = None, cookie_jar: CookieJarT = None, timeout: int = TIMEOUT) -> dict:
    url = f'/file/actions/{guid}'
    return api_request(url, method='DELETE', headers=headers, cookie_jar=cookie_jar, timeout=timeout)


def download_file(guid: str, filename: str, headers: HeaderLikeT = None, cookie_jar: CookieJarT = None, timeout: int = TIMEOUT) -> BytesIO:
    url = f'/download/{guid}/{filename}'
    res = file_request(url, method='GET', headers=headers, cookie_jar=cookie_jar, timeout=timeout)
    return res


def file_request(url: str, method='GET', data: bytes = None, headers: HeaderLikeT = None, cookie_jar: CookieJarT = None, timeout: int = TIMEOUT) -> BytesIO:
    _headers = DEFAULT_HEADERS
    if headers:
        _headers = {**_headers, **headers}
    return _base_file_request(url, method=method, data=data, headers=_headers, cookie_jar=cookie_jar, timeout=timeout)


def raw_api_request(url: str,
                    method: str = 'GET',
                    data: dict = None,
                    headers: HeaderLikeT = None,
                    cookie_jar: CookieJarT = None,
                    timeout: int = TIMEOUT) -> Tuple[dict, List]:
    resp = _base_request(**locals())
    if 200 >= resp.getcode() < 300:
        contents = resp.read()
        return json.loads(contents), resp.getheaders()
    return {}, []


def api_request(url: str, method: str = 'GET', data: Optional[dict] = None, headers: HeaderLikeT = None, cookie_jar: CookieJarT = None,
                timeout: int = TIMEOUT) -> dict:
    _data = None
    if data is not None:
        _data = str.encode(json.dumps(data), 'utf-8')
    resp = _base_request(url, method, _data, headers, cookie_jar, timeout)
    if 200 <= resp.getcode() < 500:
        return json.loads(resp.read())
    return {}
