from typing import Any, Callable, Dict, Optional, Union

import attr

from ..types import UNSET, Unset
from ..util.serialization import is_not_none


@attr.s(auto_attribs=True)
class RemoveGroupUserRequest:
    """ Must provide either `userId` or `userEmail` and `groupId` or `groupName`. """

    group_id: Union[Unset, str] = UNSET
    group_name: Union[Unset, str] = UNSET
    user_email: Union[Unset, str] = UNSET
    user_id: Union[Unset, str] = UNSET

    def to_dict(self, pick_by_predicate: Optional[Callable[[Any], bool]] = is_not_none) -> Dict[str, Any]:
        group_id = self.group_id
        group_name = self.group_name
        user_email = self.user_email
        user_id = self.user_id

        dct = {
            k: v
            for k, v in {
                "groupId": group_id,
                "groupName": group_name,
                "userEmail": user_email,
                "userId": user_id,
            }.items()
            if v != UNSET
        }
        if pick_by_predicate is not None:
            dct = {k: v for k, v in dct.items() if pick_by_predicate(v)}
        return dct

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "RemoveGroupUserRequest":
        group_id = d.get("groupId")

        group_name = d.get("groupName")

        user_email = d.get("userEmail")

        user_id = d.get("userId")

        return RemoveGroupUserRequest(
            group_id=group_id,
            group_name=group_name,
            user_email=user_email,
            user_id=user_id,
        )
