from typing import Any, Callable, Dict, Optional

import attr

from ..types import UNSET
from ..util.serialization import is_not_none


@attr.s(auto_attribs=True)
class GetQuiltCalibrationsResponse:
    """  """

    quilt: str

    def to_dict(self, pick_by_predicate: Optional[Callable[[Any], bool]] = is_not_none) -> Dict[str, Any]:
        quilt = self.quilt

        dct = {
            k: v
            for k, v in {
                "quilt": quilt,
            }.items()
            if v != UNSET
        }
        if pick_by_predicate is not None:
            dct = {k: v for k, v in dct.items() if pick_by_predicate(v)}
        return dct

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "GetQuiltCalibrationsResponse":
        quilt = d["quilt"]

        return GetQuiltCalibrationsResponse(
            quilt=quilt,
        )
