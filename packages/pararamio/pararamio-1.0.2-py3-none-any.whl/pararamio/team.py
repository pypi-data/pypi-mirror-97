from typing import Any, Dict, List, Optional, TYPE_CHECKING

from pararamio.client import Pararamio
from pararamio.exceptions import PararamioRequestException
from pararamio.user import User
from pararamio.utils import parse_datetime


if TYPE_CHECKING:
    from datetime import datetime
__all__ = ('TeamMember', 'Team')

ATTR_FORMATTERS = {
    'time_edited':  parse_datetime,
    'time_created': parse_datetime,
}
MEMBER_ATTR_FORMATTERS = {
    **ATTR_FORMATTERS,
    'last_activity': parse_datetime
}


class TeamMember:
    __slots__ = ('client', '_data')
    _data: Dict[str, Any]
    chats: List[int]
    email: str
    groups: List[int]
    id: int
    inviter_id: Optional[int]
    is_admin: bool
    is_member: bool
    last_activity: 'datetime'
    phonenumber: str
    state: str
    time_created: 'datetime'
    time_updated: 'datetime'
    two_step_enabled: bool

    def __init__(self, client: 'Pararamio', id: int, **kwargs):
        self.client = client
        self._data = {**kwargs, 'id': int(id)}

    def __getattr__(self, name):
        fmt_fnc = MEMBER_ATTR_FORMATTERS.get(name, None)
        if fmt_fnc:
            return fmt_fnc(self._data, name)
        return self._data[name]

    def __str__(self):
        text = self._data.get('text', None)
        if text is None:
            self.load()
            text = self._data['text']
        return text

    def __eq__(self, other):
        if not isinstance(other, (TeamMember, User)):
            return hash(other) == hash(self)
        return self.id == other.id

    @property
    def user(self) -> User:
        return User(client=self.client, id=self.id)


class Team:
    __slots__ = ('_data', 'client', 'load_on_key_error',)
    _data: Dict[str, Any]
    client: 'Pararamio'
    admins: List[int]
    default_thread_id: int
    description: Optional[str]
    email_domain: Optional[str]
    groups: List[int]
    guest_thread_id: Optional[int]
    guests: List[int]
    id: int
    inviter_id: Optional[int]
    is_active: bool
    slug: str
    state: str
    time_created: str
    time_updated: str
    title: str
    two_step_required: bool
    users: List[int]
    load_on_key_error: bool

    def __init__(self, client: 'Pararamio', id: int, load_on_key_error: bool = True, **kwargs):
        self.client = client
        self.load_on_key_error = load_on_key_error
        self._data = {**kwargs, 'id': int(id)}

    def __getattr__(self, name):
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
        text = self._data.get('text', None)
        if text is None:
            self.load()
            text = self._data['text']
        return text

    def __eq__(self, other):
        if not isinstance(other, Team):
            return hash(other) == hash(self)
        return self.id == other.id

    def __contains__(self, item):
        if not isinstance(item, (TeamMember, User)):
            return False
        return item.id in self.users

    def load(self):
        url = f'/core/org?ids={self.id}'
        res = self.client.api_get(url)
        self._data.update(res)
        return self

    def member_info(self, user_id: int) -> 'TeamMember':
        url = f'/core/org/{self.id}/member_info/{user_id}'
        res = self.client.api_get(url)
        if not res:
            raise PararamioRequestException('empty response for user %s', user_id)
        return TeamMember(self.client, **res)

    def members_info(self) -> List['TeamMember']:
        url = f'/core/org/{self.id}/member_info'
        res = self.client.api_get(url)
        if res:
            return [TeamMember(self.client, **m) for m in res.get('data', [])]
        return []

    @classmethod
    def my_team_ids(cls, client: 'Pararamio') -> List[int]:
        url = '/core/org/sync'
        res = client.api_get(url) or {}
        return res.pop('ids', [])

    @classmethod
    def load_teams(cls, client: 'Pararamio') -> List['Team']:
        ids = cls.my_team_ids(client)

        if ids:
            ids = ','.join(str(x) for x in ids)
            url = f'/core/org?ids={ids}'
            res = client.api_get(url)

            if res:
                return [cls(client, **r) for r in res['orgs']]

        return []
