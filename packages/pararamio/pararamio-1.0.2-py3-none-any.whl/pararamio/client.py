import logging
import mimetypes
import os
from http.cookiejar import CookieJar, FileCookieJar, LoadError, MozillaCookieJar
from io import BytesIO
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Union

from pararamio._types import ProfileTypeT, SecondStepFnT
from pararamio.chat import Chat
from pararamio.constants import XSRF_HEADER_NAME
from pararamio.exceptions import PararamioAuthenticationException, PararamioHTTPRequestException, PararamioServerResponseException, PararamioValidationException
from pararamio.file import File
from pararamio.group import Group
from pararamio.post import Post
from pararamio.user import User
from pararamio.utils.authentication import authenticate, do_second_step, do_second_step_with_code, get_xsrf_token
from pararamio.utils.helpers import check_login_opts, get_empty_vars, lazy_loader
from pararamio.utils.requests import api_request, delete_file, download_file, upload_file, xupload_file


__all__ = ('Pararamio',)
log = logging.getLogger('pararamio.client')


class Pararamio:
    _login: Optional[str]
    _password: Optional[str]
    _key: Optional[str]
    _authenticated: bool
    _cookie: Union[CookieJar, FileCookieJar]
    __profile: Optional[dict]
    __headers: Dict[str, str]
    __user: dict

    def __init__(self, login: str = None, password: str = None, key: str = None, cookie: CookieJar = None, cookie_path: str = None,
                 ignore_broken_cookie: bool = False):
        self._login = login
        self._password = password
        self._key = key
        self.__headers = {}
        self.__profile = None
        self.__user = {}
        self._authenticated = False
        if cookie is not None:
            self._cookie = cookie
        elif cookie_path is not None:
            self._cookie = MozillaCookieJar(cookie_path)
            if os.path.exists(cookie_path):
                if not os.path.isfile(cookie_path):
                    raise OSError(f'path {cookie_path} is directory')
                if not os.access(cookie_path, os.R_OK):
                    raise OSError(f'file {cookie_path} is not readable')
                if not os.access(cookie_path, os.W_OK):
                    raise OSError(f'file {cookie_path} is not writable')
                try:
                    self._cookie.load(ignore_discard=True)
                    self._authenticated = True
                except LoadError as e:
                    log.error('failed to load cookie from file %s', cookie_path)
                    if not ignore_broken_cookie:
                        raise OSError(e)
        else:
            self._cookie = CookieJar()
        for cj in self._cookie:
            if cj.name == '_xsrf':
                self.__headers[XSRF_HEADER_NAME] = str(cj.value)
                break

    def _save_cookie(self) -> None:
        if isinstance(self._cookie, FileCookieJar):
            self._cookie.save(ignore_discard=True)

    def _profile(self, raise_on_error: bool = False) -> 'ProfileTypeT':
        return self.api_get('/user/profile', raise_on_error=raise_on_error).get('message', {})

    def _do_auth(self, login: str, password: str, cookie_jar: CookieJar, headers: Dict[str, str], second_step_fn: SecondStepFnT,
                 second_step_arg: str, ) -> None:
        self._authenticated, user, xsrf = authenticate(login, password, cookie_jar, headers, second_step_fn, second_step_arg)
        if self._authenticated:
            self.__user = user
            self.__headers[XSRF_HEADER_NAME] = xsrf
            self._save_cookie()

    def _authenticate(self, login: str, password: str, second_step_fn: SecondStepFnT, second_step_arg: str) -> bool:
        if not self._cookie:
            self._do_auth(login, password, self._cookie, self.__headers, second_step_fn, second_step_arg)
        try:
            self._authenticated = True
            self._profile(raise_on_error=True)
        except PararamioHTTPRequestException:
            self._authenticated = False
            self._do_auth(login, password, self._cookie, self.__headers, second_step_fn, second_step_arg)
        return self._authenticated

    def authenticate(self, login: str = None, password: str = None, key: str = None) -> bool:
        """
        Authenticate client with totp key
        :param login: pararam login
        :param password: pararam password
        :param key: 16 chars second factor key to generate one time code
        :return: True if authentication success
        """
        login = login or self._login
        password = password or self._password
        key = key or self._key
        if not check_login_opts(login, password, key=key):
            raise PararamioAuthenticationException(f'{get_empty_vars(login=login, password=password, key=key)} must be set and not empty')
        return self._authenticate(login, password, do_second_step, key)  # type: ignore

    def authenticate_with_code(self, code: str, login: str = None, password: str = None) -> bool:
        """
        Authenticate client with generated TFA code
        :param login: pararam login
        :param password: pararam password
        :param code: 6 digits code
        :return: True if authentication success
        """
        login = login or self._login
        password = password or self._password
        if not check_login_opts(login, password, code=code):
            raise PararamioAuthenticationException(f'{get_empty_vars(login=login, password=password, code=code)} must be set and not empty')
        return self._authenticate(login, password, do_second_step_with_code, code)  # type: ignore

    def _api_request(self, url: str, method: str = 'GET', data: dict = None, callback: Callable = lambda rsp: rsp, raise_on_error: bool = False) -> Any:
        if not self._authenticated:
            self.authenticate()
        if not self.__headers.get(XSRF_HEADER_NAME, None):
            self.__headers[XSRF_HEADER_NAME] = get_xsrf_token(self._cookie)
            self._save_cookie()
        try:
            return callback(api_request(url, method, data, cookie_jar=self._cookie, headers=self.__headers))
        except PararamioHTTPRequestException as e:
            if raise_on_error:
                raise
            if e.code == 401:
                self._authenticated = False
                return self._api_request(url=url, method=method, data=data, callback=callback, raise_on_error=True)
            message = e.message
            if message == 'xsrf':
                log.info('xsrf is expire, invalid or was not set, trying to get new one')
                self.__headers[XSRF_HEADER_NAME] = ''
                return self._api_request(url=url, method=method, data=data, callback=callback, raise_on_error=True)
            raise

    def api_get(self, url: str, raise_on_error: bool = False) -> dict:
        return self._api_request(url, raise_on_error=raise_on_error)

    def api_post(self, url: str, data: Dict[Any, Any] = None, raise_on_error: bool = False) -> dict:
        return self._api_request(url, method='POST', data=data, raise_on_error=raise_on_error)

    def api_put(self, url: str, data: Dict[Any, Any] = None, raise_on_error: bool = False) -> dict:
        return self._api_request(url, method='PUT', data=data, raise_on_error=raise_on_error)

    def api_delete(self, url: str, data: Dict[Any, Any] = None, raise_on_error: bool = False) -> dict:
        return self._api_request(url, method='DELETE', data=data, raise_on_error=raise_on_error)

    @staticmethod
    def _get_file_info(file_path: str, filename: str = None, guess_type: bool = False) -> dict:
        if not os.path.exists(file_path):
            raise OSError(f'file {file_path} file does not exist')
        if not os.path.isfile(file_path):
            raise OSError(f'file {file_path} is a directory')
        if not os.access(file_path, os.R_OK):
            raise OSError(f'no read access to the {file_path} file')
        if filename is None:
            filename = os.path.basename(file_path)
        type_ = None
        if guess_type:
            if not mimetypes.inited:
                mimetypes.init(files=os.environ.get('PARARAMIO_MIME_TYPES_PATH', None))
            type_ = mimetypes.guess_type(os.path.basename(file_path))[0]
        return {
            'filename': filename,
            'size':     os.stat(file_path).st_size,
            'type':     type_
        }

    def _upload_file(self,
                     file_path: str,
                     chat_id: int,
                     filename: str = None,
                     type_: str = None,
                     organization_id: int = None,
                     reply_no: int = None,
                     quote_range: str = None):
        if not self._authenticated:
            self.authenticate()
        if not self.__headers.get(XSRF_HEADER_NAME, None):
            self.__headers[XSRF_HEADER_NAME] = get_xsrf_token(self._cookie)
        if type_ == 'organization_avatar' and organization_id is None:
            raise PararamioValidationException('organization_id must be set when type is organization_avatar')
        if type_ == 'chat_avatar' and chat_id is None:
            raise PararamioValidationException('chat_id must be set when type is chat_avatar')
        file_info = self._get_file_info(file_path, filename)
        fields = [
            ('type', type_),
            ('filename', file_info['filename']),
            ('size', file_info['size']),
            ('chat_id', chat_id),
            ('organization_id', organization_id),
            ('reply_no', reply_no),
            ('quote_range', quote_range)
        ]
        with open(file_path, 'rb') as f:
            return xupload_file(fp=f, fields=fields, headers=self.__headers, cookie_jar=self._cookie)

    def direct_upload_file(self, file_path: str, chat_id: int, filename: str = None, reply_no: int = None, quote_range: str = None) -> File:

        res = self._upload_file(file_path=file_path, chat_id=chat_id, filename=filename, reply_no=reply_no, quote_range=quote_range)
        return File(self, **res.get('data', {}))

    def upload_file(self, file_path: str, chat_id: int, filename: str = None, is_avatar=False) -> File:
        perm_url = '/file/upload'
        file_info = self._get_file_info(file_path, filename, guess_type=True)
        perm_resp = self.api_post(perm_url, {
            'is_avatar': is_avatar,
            'thread_id': chat_id,
            'file':      {
                'name': file_info['filename'],
                'type': file_info['type'],
                'size': file_info['size']
            }
        })
        if 'perm' not in perm_resp:
            raise PararamioServerResponseException('invalid server permission response %s', perm_resp)
        perm = perm_resp['perm']
        with open(file_path, 'rb') as f:
            resp = upload_file(f, perm, filename=file_info['filename'], file_type=file_info['type'], headers=self.__headers, cookie_jar=self._cookie)
        if 'data' not in resp:
            log.error('no data in response %s', resp)
            raise PararamioServerResponseException('invalid server response exception %s', resp)
        return File(self, **resp['data'])

    def delete_file(self, guid: str) -> dict:
        return delete_file(guid, headers=self.__headers, cookie_jar=self._cookie)

    def download_file(self, guid: str, filename: str) -> BytesIO:
        return download_file(guid, filename, headers=self.__headers, cookie_jar=self._cookie)

    @property
    def profile(self) -> dict:
        if not self.__profile:
            self.__profile = self._profile()
        return self.__profile

    def search_user(self, query: str) -> List[User]:
        return User.search(self, query)

    def search_group(self, query: str) -> List[Group]:
        return Group.search(self, query)

    def search_posts(self, query: str, order_type: str = 'time', page: int = 1, chat_id: int = None, limit: Optional[int] = None) -> Tuple[int, Iterable[Post]]:
        return Chat.post_search(self, query, order_type=order_type, page=page, chat_id=chat_id, limit=limit)

    def list_chats(self) -> Iterable:
        url = '/core/chat/sync'
        chats_per_load = 50
        ids = self.api_get(url).get('chats', [])
        return lazy_loader(self, ids, Chat.load_chats, per_load=chats_per_load)
