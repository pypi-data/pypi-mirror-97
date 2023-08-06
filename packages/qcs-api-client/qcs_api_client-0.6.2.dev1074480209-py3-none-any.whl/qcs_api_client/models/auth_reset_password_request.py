from typing import Any, Callable, Dict, Optional

import attr

from ..types import UNSET
from ..util.serialization import is_not_none


@attr.s(auto_attribs=True)
class AuthResetPasswordRequest:
    """  """

    new_password: str
    old_password: str

    def to_dict(self, pick_by_predicate: Optional[Callable[[Any], bool]] = is_not_none) -> Dict[str, Any]:
        new_password = self.new_password
        old_password = self.old_password

        dct = {
            k: v
            for k, v in {
                "newPassword": new_password,
                "oldPassword": old_password,
            }.items()
            if v != UNSET
        }
        if pick_by_predicate is not None:
            dct = {k: v for k, v in dct.items() if pick_by_predicate(v)}
        return dct

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AuthResetPasswordRequest":
        new_password = d["newPassword"]

        old_password = d["oldPassword"]

        return AuthResetPasswordRequest(
            new_password=new_password,
            old_password=old_password,
        )
