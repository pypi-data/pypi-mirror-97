import sys
from http.cookiejar import CookieJar
from typing import Any, Callable, Dict, Optional, Tuple, TypeVar, Union


if sys.version_info >= (3, 8):
    from typing import TypedDict


    class ProfileTypeT(TypedDict):
        unique_name: str
        id: int
        info: Optional[str]
        find_strict: bool
        name: str
        is_google: bool
        two_step_enabled: bool
        has_password: bool
        phoneconfirmed: bool
        email: str
        phonenumber: Optional[str]


    class PostMetaUserT(TypedDict):
        id: int
        name: str
        unique_name: str


    class PostMetaThreadT(TypedDict):
        title: str


    class PostMetaT(TypedDict):
        user: PostMetaUserT
        thread: PostMetaThreadT
else:
    ProfileTypeT = Dict[str, Any]
    PostMetaT = Dict[str, Any]

CookieJarT = TypeVar('CookieJarT', bound=CookieJar)
QuoteRangeT = Dict[str, Union[str, int]]
HeaderLikeT = Dict[str, str]
SecondStepFnT = Callable[[CookieJar, Dict[str, str], str], Tuple[bool, Dict[str, str]]]
