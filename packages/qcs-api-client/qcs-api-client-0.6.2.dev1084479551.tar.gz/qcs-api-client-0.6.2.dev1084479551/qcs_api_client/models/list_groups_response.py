from typing import Any, Callable, Dict, List, Optional, Union

import attr

from ..models.group import Group
from ..types import UNSET, Unset
from ..util.serialization import is_not_none


@attr.s(auto_attribs=True)
class ListGroupsResponse:
    """  """

    groups: List[Group]
    next_page_token: Union[Unset, str] = UNSET

    def to_dict(self, pick_by_predicate: Optional[Callable[[Any], bool]] = is_not_none) -> Dict[str, Any]:
        groups = []
        for groups_item_data in self.groups:
            groups_item = groups_item_data.to_dict()

            groups.append(groups_item)

        next_page_token = self.next_page_token

        dct = {
            k: v
            for k, v in {
                "groups": groups,
                "nextPageToken": next_page_token,
            }.items()
            if v != UNSET
        }
        if pick_by_predicate is not None:
            dct = {k: v for k, v in dct.items() if pick_by_predicate(v)}
        return dct

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ListGroupsResponse":
        groups = []
        _groups = d["groups"]
        for groups_item_data in _groups:
            groups_item = Group.from_dict(groups_item_data)

            groups.append(groups_item)

        next_page_token = d.get("nextPageToken")

        return ListGroupsResponse(
            groups=groups,
            next_page_token=next_page_token,
        )
