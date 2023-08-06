from typing import Any, Callable, Dict, Optional

import attr

from ..models.user_credentials_password import UserCredentialsPassword
from ..types import UNSET
from ..util.serialization import is_not_none


@attr.s(auto_attribs=True)
class UserCredentials:
    """  """

    password: UserCredentialsPassword

    def to_dict(self, pick_by_predicate: Optional[Callable[[Any], bool]] = is_not_none) -> Dict[str, Any]:
        password = self.password.to_dict()

        dct = {
            k: v
            for k, v in {
                "password": password,
            }.items()
            if v != UNSET
        }
        if pick_by_predicate is not None:
            dct = {k: v for k, v in dct.items() if pick_by_predicate(v)}
        return dct

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "UserCredentials":
        password = UserCredentialsPassword.from_dict(d["password"])

        return UserCredentials(
            password=password,
        )
