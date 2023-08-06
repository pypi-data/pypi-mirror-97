from typing import Any, Callable, Dict, Optional, Union

import attr

from ..types import UNSET, Unset
from ..util.serialization import is_not_none


@attr.s(auto_attribs=True)
class InviteUserRequest:
    """  """

    email: str
    group_name: Union[Unset, str] = UNSET

    def to_dict(self, pick_by_predicate: Optional[Callable[[Any], bool]] = is_not_none) -> Dict[str, Any]:
        email = self.email
        group_name = self.group_name

        dct = {
            k: v
            for k, v in {
                "email": email,
                "groupName": group_name,
            }.items()
            if v != UNSET
        }
        if pick_by_predicate is not None:
            dct = {k: v for k, v in dct.items() if pick_by_predicate(v)}
        return dct

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "InviteUserRequest":
        email = d["email"]

        group_name = d.get("groupName")

        return InviteUserRequest(
            email=email,
            group_name=group_name,
        )
