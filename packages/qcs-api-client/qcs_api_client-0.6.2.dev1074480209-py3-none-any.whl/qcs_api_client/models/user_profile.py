from typing import Any, Callable, Dict, Optional

import attr

from ..types import UNSET
from ..util.serialization import is_not_none


@attr.s(auto_attribs=True)
class UserProfile:
    """  """

    email: str
    first_name: str
    last_name: str
    organization: str

    def to_dict(self, pick_by_predicate: Optional[Callable[[Any], bool]] = is_not_none) -> Dict[str, Any]:
        email = self.email
        first_name = self.first_name
        last_name = self.last_name
        organization = self.organization

        dct = {
            k: v
            for k, v in {
                "email": email,
                "firstName": first_name,
                "lastName": last_name,
                "organization": organization,
            }.items()
            if v != UNSET
        }
        if pick_by_predicate is not None:
            dct = {k: v for k, v in dct.items() if pick_by_predicate(v)}
        return dct

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "UserProfile":
        email = d["email"]

        first_name = d["firstName"]

        last_name = d["lastName"]

        organization = d["organization"]

        return UserProfile(
            email=email,
            first_name=first_name,
            last_name=last_name,
            organization=organization,
        )
