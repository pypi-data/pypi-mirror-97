import datetime
from typing import Any, Callable, Dict, Optional

import attr
from dateutil.parser import isoparse
from rfc3339 import rfc3339

from ..types import UNSET
from ..util.serialization import is_not_none


@attr.s(auto_attribs=True)
class Group:
    """  """

    created_time: datetime.datetime
    description: str
    id: str
    last_membership_updated_time: datetime.datetime
    name: str
    updated_time: datetime.datetime

    def to_dict(self, pick_by_predicate: Optional[Callable[[Any], bool]] = is_not_none) -> Dict[str, Any]:
        assert self.created_time.tzinfo is not None, "Datetime must have timezone information"
        created_time = rfc3339(self.created_time)

        description = self.description
        id = self.id
        assert self.last_membership_updated_time.tzinfo is not None, "Datetime must have timezone information"
        last_membership_updated_time = rfc3339(self.last_membership_updated_time)

        name = self.name
        assert self.updated_time.tzinfo is not None, "Datetime must have timezone information"
        updated_time = rfc3339(self.updated_time)

        dct = {
            k: v
            for k, v in {
                "createdTime": created_time,
                "description": description,
                "id": id,
                "lastMembershipUpdatedTime": last_membership_updated_time,
                "name": name,
                "updatedTime": updated_time,
            }.items()
            if v != UNSET
        }
        if pick_by_predicate is not None:
            dct = {k: v for k, v in dct.items() if pick_by_predicate(v)}
        return dct

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Group":
        created_time = isoparse(d["createdTime"])

        description = d["description"]

        id = d["id"]

        last_membership_updated_time = isoparse(d["lastMembershipUpdatedTime"])

        name = d["name"]

        updated_time = isoparse(d["updatedTime"])

        return Group(
            created_time=created_time,
            description=description,
            id=id,
            last_membership_updated_time=last_membership_updated_time,
            name=name,
            updated_time=updated_time,
        )
