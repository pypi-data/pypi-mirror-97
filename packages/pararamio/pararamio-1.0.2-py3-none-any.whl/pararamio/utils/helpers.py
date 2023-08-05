import math
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence, Tuple, cast

from pararamio.constants import DATETIME_FORMAT
from pararamio.exceptions import PararamioValidationException


__all__ = ('encode_digit', 'lazy_loader', 'encode_chat_id', 'join_ids', 'parse_datetime', 'check_login_opts', 'get_empty_vars',)


def check_login_opts(login: Optional[str], password: Optional[str], **kwargs: Optional[str]) -> bool:
    return all(map(bool, [login, password, kwargs.get('code', None) or kwargs.get('key', None)]))


def get_empty_vars(**kwargs: Any):
    return ', '.join([k for k, v in kwargs.items() if not v])


def encode_digit(digit: int, res: str = '') -> str:
    if not isinstance(digit, int):
        digit = int(digit)
    code_string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_.'
    result = math.floor(digit / len(code_string))
    res = code_string[int(digit % len(code_string))] + res
    return encode_digit(result, res) if result > 0 else res


def encode_chat_id(chat_id: int, posts_count: int, last_read_post_no: int) -> str:
    return '-'.join(map(str, [chat_id, posts_count, last_read_post_no]))


def encode_chats_ids(chats_ids: List[Tuple[int, int, int]]) -> str:
    return '/'.join(map(lambda *args: encode_chat_id(*args), chats_ids))


def lazy_loader(cls: Any, items: Sequence, load_fn: Callable[[Any, List], List], per_load: int = 50) -> Iterable:
    load_counter = 0
    loaded_items: List[Any] = []
    counter = 0

    def load_items():
        return load_fn(cls, items[(per_load * load_counter): (per_load * load_counter) + per_load])

    for _ in items:
        if not loaded_items:
            loaded_items = load_items()
        if counter >= per_load:
            counter = 0
            load_counter += 1
            loaded_items = load_items()
        yield loaded_items[counter]
        counter += 1


def join_ids(items: List[Any]) -> str:
    return ','.join(map(str, items))


def get_utc(date: datetime) -> datetime:
    if date.tzinfo is None:
        raise PararamioValidationException('is not offset-aware datetime')
    return cast(datetime, date - cast(timedelta, date.utcoffset()))


def parse_datetime(data: Dict[str, Any], key: str, format_: str = DATETIME_FORMAT) -> Optional[datetime]:
    if key not in data:
        return None
    return datetime.strptime(data[key], format_).replace(tzinfo=timezone.utc)


def format_datetime(date: datetime) -> str:
    return get_utc(date).strftime(DATETIME_FORMAT)
