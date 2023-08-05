from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional, TYPE_CHECKING, Tuple, Union
from urllib.parse import quote_plus

import pararamio
from pararamio._types import QuoteRangeT
from pararamio.constants import POSTS_LIMIT
from pararamio.exceptions import PararamioLimitExceededException, PararamioMethodNotAllowed, PararamioRequestException, PararamioValidationException
from pararamio.file import File
from pararamio.post import Post
from pararamio.utils.helpers import encode_chats_ids, format_datetime, join_ids, parse_datetime


if TYPE_CHECKING:
    from pararamio.client import Pararamio
    from pararamio.user import User

__all__ = ('Chat',)

ATTR_FORMATTERS = {
    'time_edited':      parse_datetime,
    'time_created':     parse_datetime,
    'user_time_edited': parse_datetime,
}


def check_result(result: dict) -> bool:
    return 'chat_id' in result


class Chat:
    id: int
    title: str
    history_mode: str
    description: Optional[str]
    posts_count: int
    pm: bool
    e2e: bool
    time_created: datetime
    time_updated: datetime
    time_edited: Optional[datetime]
    author_id: int
    two_step_required: bool
    org_visible: bool
    organization_id: Optional[int]
    posts_live_time: Optional[int]
    allow_api: bool
    read_only: bool
    tnew: bool
    adm_flag: bool
    custom_title: Optional[str]
    is_favorite: bool
    inviter_id: Optional[int]
    tshow: bool
    user_time_edited: datetime
    admin_ids: List[int]
    history_start: int
    pinned: List[int]
    thread_groups: List[int]
    thread_users: List[int]
    thread_admins: List[int]
    members_ids: List[int]
    thread_users_all: List[int]
    last_msg_author_id: Optional[int]
    last_msg_author: str
    last_msg_bot_name: str
    last_msg_text: str
    last_msg: str
    last_read_post_no: int
    guests: List[int]
    thread_guests: List[int]
    _data: Dict[str, Any]
    _client: 'Pararamio'
    load_on_key_error: bool

    def __init__(self, client: 'Pararamio', id: int = None, load_on_key_error: bool = True, **kwargs):
        if id is None:
            id = kwargs.get('chat_id', None)
            if id is None:
                id = kwargs['thread_id']
        self.id = int(id)
        self._data = {}
        if kwargs:
            self._data = {**kwargs, 'id': id}
        self.load_on_key_error = load_on_key_error
        self._client = client

    def __getattr__(self, name: str):
        fmt_fnc = ATTR_FORMATTERS.get(name, None)
        if fmt_fnc:
            return fmt_fnc(self._data, name)
        try:
            return self._data[name]
        except KeyError:
            if self.load_on_key_error:
                self.load()
                return self._data[name]
            raise

    def __str__(self):
        title = self._data.get('title', '')
        id_ = self.id or ''
        return f'{id_} - {title}'

    def __eq__(self, other: object):
        if not isinstance(other, Chat):
            return id(other) == id(self)
        return self.id == other.id

    def __contains__(self, item: Union[Post, 'User']) -> bool:
        if isinstance(item, Post):
            return item.chat == self
        if isinstance(item, pararamio.user.User):
            return item.id in self.members_ids
        return False

    @property
    def client(self) -> 'Pararamio':
        return self._client

    def load(self) -> 'Chat':
        if self.id is None:
            raise PararamioMethodNotAllowed(f'Load is not allow for new {self.__class__.__name__}')
        chats = self.load_chats(self._client, [self.id])
        if len(chats) != 1:
            raise PararamioRequestException(f'failed to load data for chat id {self.id}')
        self._data = chats[0]._data
        return self

    def edit(self, **kwargs) -> None:
        """
        :param kwargs:
        available args
        {
            "title": "My title",
            "description": "Description",
            "posts_live_time": null,  // null,int,float sec
            "two_step_required": false,
            "history_mode": "all",
            "cover_path": null,
            "org_visible": false,
            "allow_api": true,
            "read_only": false
        }
        :return:
        """
        url = f'/core/chat/{self.id}'
        check_result(self._client.api_put(url, data=kwargs))

    def transfer(self, org_id: int) -> bool:
        url = f'/core/chat/{self.id}/transfer/{org_id}'
        return check_result(self._client.api_post(url, {}))

    def delete(self):
        url = f'/core/chat/{self.id}'
        return check_result(self._client.api_delete(url))

    def hide(self) -> bool:
        url = f'/core/chat/{self.id}/hide'
        return check_result(self._client.api_post(url))

    def show(self) -> bool:
        url = f'/core/chat/{self.id}/show'
        return check_result(self._client.api_post(url))

    def favorite(self) -> bool:
        url = f'/core/chat/{self.id}/favorite'
        return check_result(self._client.api_post(url))

    def unfavorite(self) -> bool:
        url = f'/core/chat/{self.id}/unfavorite'
        return check_result(self._client.api_post(url))

    def enter(self) -> bool:
        url = f'/core/chat/{self.id}/enter'
        return check_result(self._client.api_post(url))

    def quit(self) -> bool:
        url = f'/core/chat/{self.id}/quit'
        return check_result(self._client.api_post(url))

    def set_custom_title(self, title: str) -> bool:
        url = f'/core/chat/{self.id}/custom_title'
        return check_result(self._client.api_post(url, {'title': title}))

    def sync(self) -> None:
        # url = '/core/chat/sync'
        # return self.client.api_post(url, {
        #    'ids':       encode_chat_id(self.id, self._data.get('posts_count', 0), self._data.get('last_read_post_no', 0)),
        #    'sync_time': self._data.get('time_updated', datetime.now().strftime(DATETIME_FORMAT))
        # })
        # TODO: Implement sync
        raise NotImplementedError()

    def add_users(self, ids: List[int]) -> bool:
        url = f'/core/chat/{self.id}/user/{join_ids(ids)}'
        return check_result(self._client.api_post(url))

    def delete_users(self, ids: List[int]) -> bool:
        url = f'/core/chat/{self.id}/user/{join_ids(ids)}'
        return check_result(self._client.api_delete(url))

    def add_admins(self, ids: List[int]) -> bool:
        url = f'/core/chat/{self.id}/admin/{join_ids(ids)}'
        return check_result(self._client.api_post(url))

    def delete_admins(self, ids: List[int]) -> bool:
        url = f'/core/chat/{self.id}/admin/{join_ids(ids)}'
        return check_result(self._client.api_delete(url))

    def add_groups(self, ids: List[int]) -> bool:
        url = f'/core/chat/{self.id}/group/{join_ids(ids)}'
        return check_result(self._client.api_post(url))

    def delete_groups(self, ids: List[int]) -> bool:
        url = f'/core/chat/{self.id}/group/{join_ids(ids)}'
        return check_result(self._client.api_delete(url))

    def posts(self, start_post_no: int = -50, end_post_no: int = -1) -> List['Post']:
        url = f'/msg/post?chat_id={self.id}&range={start_post_no}x{end_post_no}'
        if (start_post_no < 0 <= end_post_no) or (start_post_no >= 0 > end_post_no):
            raise PararamioValidationException('start_post_no and end_post_no can only be negative or positive at the same time')
        if 0 > start_post_no > end_post_no:
            raise PararamioValidationException('range start_post_no must be greater then end_post_no')
        if 0 <= start_post_no > end_post_no:
            raise PararamioValidationException('range start_post_no must be smaller then end_post_no')
        _absolute = abs(end_post_no - start_post_no)
        if start_post_no < 0:
            _absolute = + 1
        if _absolute > POSTS_LIMIT:
            raise PararamioLimitExceededException('max post load limit is {}'.format(POSTS_LIMIT))
        res = self._client.api_get(url).get('posts', [])
        if not res:
            return []
        return [Post(chat=self, **post) for post in res]

    def read_status(self, post_no: int) -> bool:
        url = f'/msg/lastread/{self.id}'
        res = self._client.api_post(url, {'post_no': post_no})
        if not res:
            return False
        if 'post_no' in res:
            self._data['last_read_post_no'] = res['post_no']
        if 'posts_count' in res:
            self._data['posts_count'] = res['posts_count']
        return True

    def post(self, text: str, quote_range: QuoteRangeT = None, reply_no: int = None, file: File = None) -> 'Post':
        if self.id is None:
            raise ValueError('can not post file to new chat')
        return Post.create(self, text=text, reply_no=reply_no, quote_range=quote_range, file=file)

    def direct_upload_file(self, file_path: str, filename: str = None, reply_no: int = None, quote_range: str = None) -> File:
        if self.id is None:
            raise ValueError('can not upload file to new chat')
        return self._client.direct_upload_file(file_path=file_path, chat_id=self.id, filename=filename, reply_no=reply_no, quote_range=quote_range)

    def upload_file(self, file_path: str, filename: str = None) -> File:
        if self.id is None:
            raise ValueError('can not upload file to new chat')
        return self._client.upload_file(file_path=file_path, chat_id=self.id, filename=filename)

    @classmethod
    def load_chats(cls, client: 'Pararamio', ids: List[int]) -> List['Chat']:
        url = f'/core/chat?ids={join_ids(ids)}'
        res = client.api_get(url)
        if res and 'chats' in res:
            return [cls(client, **data) for data in client.api_get(url).get('chats', [])]
        raise PararamioRequestException('failed to load data for chats ids: {}'.format(','.join(map(str, ids))))

    @classmethod
    def post_search(cls,
                    client: 'Pararamio',
                    q: str,
                    order_type: str = 'time',
                    page: int = 1,
                    chat_id: int = None,
                    limit: Optional[int] = POSTS_LIMIT) -> Tuple[int, Iterable['Post']]:
        if not limit:
            limit = POSTS_LIMIT
        url = f'/posts/search?q={quote_plus(q)}&order_type={order_type}&page={page}&limit={limit}'
        if chat_id is not None:
            url += f'&th_id={chat_id}'

        res = client.api_get(url)
        if 'posts' not in res:
            raise PararamioRequestException('failed to perform search')
        created_chats = {}

        def create_post(data):
            nonlocal created_chats
            _chat_id = data['thread_id']
            post_no = data['post_no']
            if _chat_id not in created_chats:
                created_chats[_chat_id] = cls(client, id=_chat_id)
            return Post(created_chats[_chat_id], post_no=post_no)

        return res['count'], map(create_post, res['posts'])

    @classmethod
    def create(cls, client: 'Pararamio', title: str, description: str = '', users: List[int] = None, groups: List[int] = None, **kwargs) -> 'Chat':
        """
        Create new chat in pararam
        :param client:
        :param title:
        :param description:
        :param users:
        :param groups:
        :param kwargs: available
        {
            "organization_id": null,  // null,int
            "posts_live_time": null,  // null,int,float sec
            "two_step_required": false,
            "cover_path": null,
            "history_mode": "all",
            "org_visible": false,
            "allow_api": true,
            "read_only": false,
        }
        :return:
        """
        if users is None:
            users = []
        if groups is None:
            groups = []
        data = {'title': title, 'description': description, 'users': users, 'groups': groups, **kwargs}

        res = client.api_post('/core/chat', data)
        id_: int = res['chat_id']
        return cls(client, id_)

    @classmethod
    def create_private_chat(cls, client: 'Pararamio', user_id: int) -> 'Chat':
        url = f'/core/chat/pm/{user_id}'
        res = client.api_post(url)
        id_: int = res['chat_id']
        return cls(client, id=id_)

    @staticmethod
    def sync_chats(client: 'Pararamio', chats_ids: List[Tuple[int, int, int]], sync_time: datetime = None) -> Dict[str, Any]:
        """

        :param client:
        :param chats_ids: List[Tuple[chat_id,posts_count,last_read_post_no]
        :param sync_time: updates from this time
        :return: {
            "new": int[],   // список чатов с tshow=True, но не преданных с клиента
            "updated": int[],  // список чатов с tshow=True и time_edited > sync_time
            "removed": int[], // список чатов переданных с клиента, но не найденных с фильтром tshow=True
            "status": {  // тут будут статусы чатов, если они не совпадают с переданными
                123: {  // chat_id
                    "posts_count": 47,
                    "last_read_post_no": 45,
                    "last_msg": "vlasov: фыв",
                    "time_updated": "2018-08-23T09:18:56.143850Z"
                },
               ...
            }

        """
        url = '/core/chat/sync'
        data = {
            'ids': encode_chats_ids(chats_ids)
        }
        if sync_time:
            data['sync_time'] = format_datetime(sync_time)
        return client.api_post(url)
