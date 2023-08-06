from typing import Any, Callable, Dict, Optional

import attr

from ..types import UNSET
from ..util.serialization import is_not_none


@attr.s(auto_attribs=True)
class AuthResetPasswordWithTokenRequest:
    """ Token may be requested with AuthEmailPasswordResetToken. """

    new_password: str
    token: str

    def to_dict(self, pick_by_predicate: Optional[Callable[[Any], bool]] = is_not_none) -> Dict[str, Any]:
        new_password = self.new_password
        token = self.token

        dct = {
            k: v
            for k, v in {
                "newPassword": new_password,
                "token": token,
            }.items()
            if v != UNSET
        }
        if pick_by_predicate is not None:
            dct = {k: v for k, v in dct.items() if pick_by_predicate(v)}
        return dct

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AuthResetPasswordWithTokenRequest":
        new_password = d["newPassword"]

        token = d["token"]

        return AuthResetPasswordWithTokenRequest(
            new_password=new_password,
            token=token,
        )
