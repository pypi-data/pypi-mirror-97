from typing import Any, Dict, List, TYPE_CHECKING


if TYPE_CHECKING:
    from pararamio.client import Pararamio

__all__ = ('Group',)


class Group:
    id: int
    _data: Dict[str, Any]
    _client: 'Pararamio'

    def __init__(self, client: 'Pararamio', id: int, **kwargs):
        self.id = id
        self._data = {}
        if kwargs:
            self._data = {'id': id, **kwargs}
        self._client = client

    def __getattr__(self, name: str) -> Any:
        return self._data[name]

    def __str__(self) -> str:
        title = self.title or 'New'
        id_ = self.id or ''
        return f'[{id_}] {title}'

    def __eq__(self, other) -> bool:
        if not isinstance(other, Group):
            return id(other) == id(self)
        return self.id == other.id

    def sync(self):
        # TODO: Implement sync
        raise NotImplementedError()

    @classmethod
    def search(cls, client: 'Pararamio', search_string: str) -> List['Group']:
        url = f'/users?flt={search_string}'
        return [cls(client, **group) for group in client.api_get(url).get('groups', [])]
