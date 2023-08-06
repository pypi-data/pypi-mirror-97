from typing import Any, Callable, Dict, List, Optional, Union

import attr

from ..models.user import User
from ..types import UNSET, Unset
from ..util.serialization import is_not_none


@attr.s(auto_attribs=True)
class ListGroupUsersResponse:
    """  """

    users: List[User]
    next_page_token: Union[Unset, str] = UNSET

    def to_dict(self, pick_by_predicate: Optional[Callable[[Any], bool]] = is_not_none) -> Dict[str, Any]:
        users = []
        for users_item_data in self.users:
            users_item = users_item_data.to_dict()

            users.append(users_item)

        next_page_token = self.next_page_token

        dct = {
            k: v
            for k, v in {
                "users": users,
                "nextPageToken": next_page_token,
            }.items()
            if v != UNSET
        }
        if pick_by_predicate is not None:
            dct = {k: v for k, v in dct.items() if pick_by_predicate(v)}
        return dct

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ListGroupUsersResponse":
        users = []
        _users = d["users"]
        for users_item_data in _users:
            users_item = User.from_dict(users_item_data)

            users.append(users_item)

        next_page_token = d.get("nextPageToken")

        return ListGroupUsersResponse(
            users=users,
            next_page_token=next_page_token,
        )
