from typing import Any, Callable, Dict, Optional

import attr

from ..types import UNSET
from ..util.serialization import is_not_none


@attr.s(auto_attribs=True)
class CheckClientApplicationResponse:
    """  """

    is_latest_version: bool
    is_update_required: bool
    message: str

    def to_dict(self, pick_by_predicate: Optional[Callable[[Any], bool]] = is_not_none) -> Dict[str, Any]:
        is_latest_version = self.is_latest_version
        is_update_required = self.is_update_required
        message = self.message

        dct = {
            k: v
            for k, v in {
                "isLatestVersion": is_latest_version,
                "isUpdateRequired": is_update_required,
                "message": message,
            }.items()
            if v != UNSET
        }
        if pick_by_predicate is not None:
            dct = {k: v for k, v in dct.items() if pick_by_predicate(v)}
        return dct

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "CheckClientApplicationResponse":
        is_latest_version = d["isLatestVersion"]

        is_update_required = d["isUpdateRequired"]

        message = d["message"]

        return CheckClientApplicationResponse(
            is_latest_version=is_latest_version,
            is_update_required=is_update_required,
            message=message,
        )
