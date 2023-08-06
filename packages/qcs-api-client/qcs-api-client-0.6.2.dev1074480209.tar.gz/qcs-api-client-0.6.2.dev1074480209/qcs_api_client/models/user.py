import datetime
from typing import Any, Callable, Dict, Optional, Union, cast

import attr
from dateutil.parser import isoparse
from rfc3339 import rfc3339

from ..models.user_profile import UserProfile
from ..types import UNSET, Unset
from ..util.serialization import is_not_none


@attr.s(auto_attribs=True)
class User:
    """  """

    created_time: datetime.datetime
    id: int
    idp_id: str
    profile: Union[UserProfile, Unset] = UNSET

    def to_dict(self, pick_by_predicate: Optional[Callable[[Any], bool]] = is_not_none) -> Dict[str, Any]:
        assert self.created_time.tzinfo is not None, "Datetime must have timezone information"
        created_time = rfc3339(self.created_time)

        id = self.id
        idp_id = self.idp_id
        profile: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.profile, Unset):
            profile = self.profile.to_dict()

        dct = {
            k: v
            for k, v in {
                "createdTime": created_time,
                "id": id,
                "idpId": idp_id,
                "profile": profile,
            }.items()
            if v != UNSET
        }
        if pick_by_predicate is not None:
            dct = {k: v for k, v in dct.items() if pick_by_predicate(v)}
        return dct

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "User":
        created_time = isoparse(d["createdTime"])

        id = d["id"]

        idp_id = d["idpId"]

        profile: Union[UserProfile, Unset] = UNSET
        _profile = d.get("profile")
        if _profile is not None and not isinstance(_profile, Unset):
            profile = UserProfile.from_dict(cast(Dict[str, Any], _profile))

        return User(
            created_time=created_time,
            id=id,
            idp_id=idp_id,
            profile=profile,
        )
