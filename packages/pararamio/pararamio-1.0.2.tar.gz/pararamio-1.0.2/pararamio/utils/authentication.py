import base64
import binascii
import hashlib
import hmac
import json
import logging
import time
from datetime import datetime
from http.cookiejar import CookieJar
from typing import Any, Dict, Tuple
from urllib.error import HTTPError

from pararamio._types import HeaderLikeT, SecondStepFnT
from pararamio.constants import XSRF_HEADER_NAME
from pararamio.exceptions import PararamioAuthenticationException, PararamioXSFRRequestError
from pararamio.utils.requests import api_request, raw_api_request


__all__ = ('get_xsrf_token', 'authenticate', 'do_second_step', 'do_second_step_with_code',)

XSFR_URL = INIT_URL = '/auth/init'
LOGIN_URL = '/auth/login/password'
TWO_STEP_URL = '/auth/totp'
AUTH_URL = '/auth/next'
log = logging.getLogger('pararamio')


def get_xsrf_token(cookie_jar: CookieJar) -> str:
    _, headers = raw_api_request(XSFR_URL, cookie_jar=cookie_jar)
    for key, value in headers:
        if key == 'X-Xsrftoken':
            return value
    raise PararamioXSFRRequestError('XSFR Header was not found in %s url' % XSFR_URL)


def do_init(cookie_jar: CookieJar, headers: dict) -> Tuple[bool, dict]:
    try:
        return True, api_request(
            INIT_URL,
            method='GET',
            headers=headers,
            cookie_jar=cookie_jar,
        )
    except HTTPError as e:
        if e.code < 500:
            return False, json.loads(e.read())
        raise


def do_login(login: str, password: str, cookie_jar: CookieJar, headers: dict) -> Tuple[bool, dict]:
    try:
        return True, api_request(
            LOGIN_URL,
            method='POST',
            data={'email': login, 'password': password},
            headers=headers,
            cookie_jar=cookie_jar,
        )
    except HTTPError as e:
        if e.code < 500:
            return False, json.loads(e.read())
        raise


def do_taking_secret(cookie_jar: CookieJar, headers: dict) -> Tuple[bool, dict]:
    try:
        return True, api_request(
            AUTH_URL,
            method='GET',
            headers=headers,
            cookie_jar=cookie_jar,
        )
    except HTTPError as e:
        if e.code < 500:
            return False, json.loads(e.read())
        raise


def do_second_step(cookie_jar: CookieJar, headers: dict, key: str) -> Tuple[bool, Dict[str, str]]:
    """
    do second step pararam login with TFA key or raise Exception
    :param cookie_jar: cookie container
    :param headers: headers to send
    :param key: key to generate one time code
    :return: True if login success
    """
    if not key:
        raise PararamioAuthenticationException('key can not be empty')
    try:
        key = generate_otp(key)
    except binascii.Error:
        raise PararamioAuthenticationException('Invalid second step key')
    resp = api_request(
        TWO_STEP_URL,
        method='POST',
        data={'code': key},
        headers=headers,
        cookie_jar=cookie_jar,
    )
    return True, resp


def do_second_step_with_code(cookie_jar: CookieJar, headers: Dict[str, str], code: str) -> Tuple[bool, Dict[str, str]]:
    """
    do second step pararam login with TFA code or raise Exception
    :param cookie_jar: cookie container
    :param headers: headers to send
    :param code: 6 digits code
    :return:  True if login success
    """
    if not code:
        raise PararamioAuthenticationException('code can not be empty')
    if len(code) != 6:
        raise PararamioAuthenticationException('code must be 6 digits len')
    resp = api_request(
        TWO_STEP_URL,
        method='POST',
        data={'code': code},
        headers=headers,
        cookie_jar=cookie_jar,
    )
    return True, resp


def authenticate(login: str,
                 password: str,
                 cookie_jar: CookieJar,
                 headers: HeaderLikeT = None,
                 second_step_fn: SecondStepFnT = do_second_step,
                 second_step_arg: str = None
                 ) -> Tuple[bool, Dict[str, Any], str]:
    if not headers or XSRF_HEADER_NAME not in headers:
        if headers is None:
            headers = {}
        headers[XSRF_HEADER_NAME] = get_xsrf_token(cookie_jar)

    success, resp = do_login(login, password, cookie_jar, headers)

    if resp.get('codes', {}).get('non_field', '') == 'captcha_required':
        try:
            from pararamio.utils.captcha import show_captcha

            success = show_captcha(f'login:{login}', headers, cookie_jar)
            if not success:
                raise PararamioAuthenticationException('Captcha required')
            else:
                success, resp = do_login(login, password, cookie_jar, headers)
        except ImportError:
            raise PararamioAuthenticationException('Captcha required, but exception when show it')

    if not success and resp.get('error', 'xsrf'):
        log.debug('invalid xsrf trying to get new one')
        headers[XSRF_HEADER_NAME] = get_xsrf_token(cookie_jar)
        success, resp = do_login(login, password, cookie_jar, headers)

    if not success:
        log.error('authentication failed: %s', resp.get('error', ''))
        raise PararamioAuthenticationException('Login, password authentication failed')

    if second_step_fn and second_step_arg:
        success, resp = second_step_fn(cookie_jar, headers, second_step_arg)
        if not success:
            raise PararamioAuthenticationException('Second factor authentication failed')

    success, resp = do_taking_secret(cookie_jar, headers)

    if not success:
        raise PararamioAuthenticationException('Taking secret failed')

    success, resp = do_init(cookie_jar, headers)

    return True, {'user_id': resp.get('user_id')}, headers[XSRF_HEADER_NAME]


def generate_otp(key: str) -> str:
    digits = 6
    digest = hashlib.sha1
    interval = 30

    def byte_secret(s):
        missing_padding = len(s) % 8
        if missing_padding != 0:
            s += '=' * (8 - missing_padding)
        return base64.b32decode(s, casefold=True)

    def int_to_byte_string(i, padding=8):
        result = bytearray()
        while i != 0:
            result.append(i & 0xFF)
            i >>= 8
        return bytes(bytearray(reversed(result)).rjust(padding, b'\0'))

    def time_code(for_time):
        i = time.mktime(for_time.timetuple())
        return int(i / interval)

    hmac_hash = hmac.new(
        byte_secret(key),
        int_to_byte_string(time_code(datetime.now())),
        digest,
    ).digest()

    hmac_hash = bytearray(hmac_hash)
    offset = hmac_hash[-1] & 0xf
    code = ((hmac_hash[offset] & 0x7f) << 24 | (hmac_hash[offset + 1] & 0xff) << 16 | (hmac_hash[offset + 2] & 0xff) << 8 | (hmac_hash[offset + 3] & 0xff))
    str_code = str(code % 10 ** digits)
    while len(str_code) < digits:
        str_code = '0' + str_code

    return str_code
