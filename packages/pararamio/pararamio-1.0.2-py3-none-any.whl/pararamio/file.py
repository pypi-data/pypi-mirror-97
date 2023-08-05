from typing import Any, Callable, Dict, TYPE_CHECKING

from pararamio.exceptions import PararamioValidationException


if TYPE_CHECKING:
    from pararamio.client import Pararamio
ATTR_FORMATTERS: Dict[str, Callable[[dict, str], Any]] = {}


class File:
    """
    {
     "data":
      {"path": "4faf5a45c5ba447ab7004b30181dd4c1/image.jpg",
       "name": "image.jpg",
       "source": "upload",
       "size": 2845000,
       "guid": "4faf5a45c5ba447ab7004b30181dd4c1",
       "up_time": "2017-08-23 12:11:54,161837",
       "id": 435,
       "type": "image/jpeg"},
     "status": "success"
    }
    """
    _client: 'Pararamio'
    _data: Dict[str, Any]
    guid: str

    def __init__(self, client, guid: str, **kwargs):
        self._client = client
        self.guid = guid
        self._data = {**kwargs, 'guid': guid}
        if 'name' in kwargs:
            self._data['filename'] = kwargs['name']

    def __getattr__(self, name):
        fmt_fnc = ATTR_FORMATTERS.get(name, None)
        if fmt_fnc:
            return fmt_fnc(self._data, name)
        return self._data[name]

    def __str__(self):
        return self._data.get('name', '')

    def serialize(self) -> Dict[str, str]:
        return self._data

    def delete(self):
        self._client.delete_file(self.guid)

    def download(self, filename: str = None):
        if filename is None and 'filename' not in self._data:
            raise PararamioValidationException('can not determine filename')
        self._client.download_file(self.guid, filename or self._data['filename'])
