from typing import Any, Dict, List, Optional, TYPE_CHECKING, Union

from pararamio.chat import Chat
from pararamio.exceptions import PararamioRequestException
from pararamio.file import File
from pararamio.post import Post
from pararamio.utils.helpers import join_ids


if TYPE_CHECKING:
    from pararamio.client import Pararamio

__all__ = ('User',)


class User:
    __slots__ = ('_data', '_client', 'id', 'load_on_key_error',)
    id: int
    info: Optional[str]
    organizations: List[int]
    unique_name: str
    info_about_user: Optional[List[Dict[str, Any]]]
    name: str
    deleted: bool
    info_about_user_parsed: Optional[str]
    active: bool
    name_trans: str
    info_parsed: Optional[List[Dict[str, Any]]]
    _data: Dict[str, Any]
    _client: 'Pararamio'
    load_on_key_error: bool

    def __init__(self, client, id: int, load_on_key_error: bool = True, **kwargs):
        self._client = client
        self.id = id
        self._data = {'id': id, **kwargs}
        self.load_on_key_error = load_on_key_error

    def __getattr__(self, name):
        try:
            return self._data[name]
        except KeyError:
            if self.load_on_key_error:
                self.load()
                return self._data[name]
            raise

    def __eq__(self, other):
        if not isinstance(other, User):
            return id(other) == id(self)
        return self.id == other.id

    @property
    def has_pm(self):
        if hasattr(self, 'pm_thread_id') and self.pm_thread_id is not None:
            return True
        return False

    def get_pm_thread(self) -> Chat:
        pm_thread_id = self._data.get('pm_thread_id', None)
        if pm_thread_id is not None:
            chat = Chat(self._client, pm_thread_id)
            return chat
        return Chat.create_private_chat(self._client, self.id)

    def load(self) -> 'User':
        res = self._load_users_request(self._client, [self.id])
        if len(res) != 1:
            raise PararamioRequestException()
        self._data = {'id': self.id, **res[0]}
        return self

    @classmethod
    def _load_users_request(cls, client: 'Pararamio', ids: List[int]) -> dict:
        url = f'/user?ids={join_ids(ids)}'
        return client.api_get(url).get('users', [])

    @classmethod
    def load_users(cls, client, ids: List[int]) -> List['User']:
        return [cls(client, **user) for user in cls._load_users_request(client, ids)]

    def post(self, text: str, quote_range: Dict[str, Union[str, int]] = None, reply_no: int = None, file: File = None) -> Post:
        chat = self.get_pm_thread()
        return chat.post(text=text, quote_range=quote_range, reply_no=reply_no, file=file)

    def __str__(self):
        if 'name' not in self._data:
            self.load()
        return self._data.get('name')

    @classmethod
    def search(cls, client: 'Pararamio', search_string: str) -> List['User']:
        url = f'/users?flt={search_string}'
        return [cls(client, **user) for user in client.api_get(url).get('users', [])]
