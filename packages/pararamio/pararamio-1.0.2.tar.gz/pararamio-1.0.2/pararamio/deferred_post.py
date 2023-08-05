from datetime import datetime, timezone
from typing import List, Optional

from pararamio._types import QuoteRangeT
from pararamio.client import Pararamio
from pararamio.utils.helpers import format_datetime, parse_datetime


__all__ = ('DeferredPost',)
ATTR_FORMATTERS = {
    'time_created': parse_datetime,
    'time_sending': lambda data, key: datetime.fromtimestamp(data['data'][key], tz=timezone.utc)
}


class DeferredPost:
    """
    {
            "id": 1,
            "user_id": 1,
            "chat_id": 27,
            "data": {  // данные для обработки, дублируются
                "user_id": 1,
                "chat_id": 27,
                "text": "deferred post",
                "reply_no": null,
                "quote_range": null
            },
            "time_created": "2019-10-16T11:09:39.011395Z",
            "time_sending": "2019-10-17T00:00:00Z"
        }
    """
    id: int
    user_id: int
    chat_id: int
    text: str
    reply_no: Optional[int]
    time_created: datetime
    time_sending: datetime
    _data: dict
    _client: 'Pararamio'

    def __init__(self, client: 'Pararamio', id: int, **kwargs):
        self._client = client
        self.id = id
        self._data = {'id': id, **kwargs}

    def __getattr__(self, name):
        fmt_fnc = ATTR_FORMATTERS.get(name, None)
        if fmt_fnc:
            return fmt_fnc(self._data, name)
        if name in self._data.get('data', {}):
            return self._data['data'][name]
        return self._data[name]

    def __str__(self):
        text = self._data.get('text', None)
        if text is None:
            self.load()
            text = self._data['text']
        return text

    def delete(self):
        url = f'/msg/deferred/{self.id}'
        self._client.api_delete(url)

    @classmethod
    def create(cls, client: 'Pararamio', chat_id: int, text: str, time_sending: datetime, reply_no: int = None,
               quote_range: QuoteRangeT = None) -> 'DeferredPost':
        url = '/msg/deferred'
        data = {
            'chat_id':      chat_id,
            'text':         text,
            'time_sending': format_datetime(time_sending),
            'reply_no':     reply_no,
            'quote_range':  quote_range
        }
        res = client.api_post(url, data)
        return cls(client, id=int(res['deferred_post_id']), **{
            'chat_id':      chat_id,
            'data':         data,
            "time_sending": data['time_sending']
        })

    @classmethod
    def get_deferred_posts(cls, client: 'Pararamio') -> List['DeferredPost']:
        url = '/msg/deferred'
        res = client.api_get(url).get('posts', [])
        return [cls(client, **post) for post in res]
