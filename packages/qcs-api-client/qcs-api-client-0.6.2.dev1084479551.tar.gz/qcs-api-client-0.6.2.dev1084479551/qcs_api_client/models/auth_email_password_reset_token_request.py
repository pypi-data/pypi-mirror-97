from typing import Any, Callable, Dict, Optional

import attr

from ..types import UNSET
from ..util.serialization import is_not_none


@attr.s(auto_attribs=True)
class AuthEmailPasswordResetTokenRequest:
    """  """

    email: str

    def to_dict(self, pick_by_predicate: Optional[Callable[[Any], bool]] = is_not_none) -> Dict[str, Any]:
        email = self.email

        dct = {
            k: v
            for k, v in {
                "email": email,
            }.items()
            if v != UNSET
        }
        if pick_by_predicate is not None:
            dct = {k: v for k, v in dct.items() if pick_by_predicate(v)}
        return dct

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AuthEmailPasswordResetTokenRequest":
        email = d["email"]

        return AuthEmailPasswordResetTokenRequest(
            email=email,
        )
