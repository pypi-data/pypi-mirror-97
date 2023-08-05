from typing import Any, Callable, Dict, Iterable, List, Optional, Union

from pararamio.exceptions import PararamioRequestException
from pararamio.utils import bot_request, join_ids, lazy_loader


__all__ = ('PararamioBot',)


def _load_chats(cls, ids: List[int]) -> List[Dict[str, Any]]:
    url = f'/core/chat?ids={join_ids(ids)}'
    res = cls.request(url)
    if res and 'chats' in res:
        return [data for data in cls.request(url).get('chats', [])]
    raise PararamioRequestException('failed to load data for chats ids: {}'.format(','.join(map(str, ids))))


def _one_or_value_error(fn: Callable, msg: str, *args) -> Any:
    try:
        return fn()[0]
    except IndexError:
        pass
    raise ValueError(msg.format(*args))


class PararamioBot:
    key: str

    def __init__(self, key: str):
        if len(key) > 50:
            key = key[20:]
        self.key = key

    def request(self, url: str, method: str = 'GET', data: Optional[dict] = None, headers: dict = None) -> Dict:
        return bot_request(url, self.key, method=method, data=data, headers=headers)

    def post_message(self, chat_id: int, text: str, reply_no: Optional[int] = None) -> Dict[str, Union[str, int]]:
        url = '/bot/message'
        return self.request(url, method='POST', data={'chat_id': chat_id, 'text': text, 'reply_no': reply_no})

    def post_private_message_by_user_id(self, user_id: int, text: str) -> Dict[str, Union[str, int]]:
        url = '/msg/post/private'
        return self.request(url, method='POST', data={'text': text, 'user_id': user_id})

    def post_private_message_by_user_email(self, email: str, text: str) -> Dict[str, Union[str, int]]:
        url = '/msg/post/private'
        return self.request(url, method='POST', data={'text': text, 'user_email': email})

    def get_tasks(self) -> Dict[str, Any]:
        url = '/msg/task'
        return self.request(url)

    def set_task_status(self, chat_id: int, post_no: int, state: str) -> Dict:
        if str.lower(state) not in ('open', 'done', 'close'):
            raise ValueError(f'unknown state {state}')
        url = f'/msg/task/{chat_id}/{post_no}'
        data = {'state': state}
        return self.request(url, method='POST', data=data)

    def get_chat(self, chat_id) -> Dict[str, Any]:
        url = f'/core/chat?ids={chat_id}'
        return _one_or_value_error(lambda: self.request(url).get('chats', []), 'chat with id {0} is not found', chat_id)

    def get_chats(self) -> Iterable[dict]:
        url = '/core/chat/sync'
        chats_per_load = 50
        ids = self.request(url).get('chats', [])
        return lazy_loader(self, ids, _load_chats, per_load=chats_per_load)

    def get_users(self, users_ids: List[int]) -> Dict[str, Any]:
        url = f'/core/user?ids={join_ids(users_ids)}'
        return self.request(url).get('users', [])

    def get_user_by_id(self, user_id: int):
        return _one_or_value_error(lambda: self.get_users([user_id]), 'user with id {0} is not found', user_id)
