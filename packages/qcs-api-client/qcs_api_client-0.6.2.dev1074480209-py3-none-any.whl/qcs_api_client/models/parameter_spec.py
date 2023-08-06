from typing import Any, Callable, Dict, Optional, Union

import attr

from ..types import UNSET, Unset
from ..util.serialization import is_not_none


@attr.s(auto_attribs=True)
class ParameterSpec:
    """  """

    length: Union[Unset, int] = UNSET

    def to_dict(self, pick_by_predicate: Optional[Callable[[Any], bool]] = is_not_none) -> Dict[str, Any]:
        length = self.length

        dct = {
            k: v
            for k, v in {
                "length": length,
            }.items()
            if v != UNSET
        }
        if pick_by_predicate is not None:
            dct = {k: v for k, v in dct.items() if pick_by_predicate(v)}
        return dct

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ParameterSpec":
        length = d.get("length")

        return ParameterSpec(
            length=length,
        )
