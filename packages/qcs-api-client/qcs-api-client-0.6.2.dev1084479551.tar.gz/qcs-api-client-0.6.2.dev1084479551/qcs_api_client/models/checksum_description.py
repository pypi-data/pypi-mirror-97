from typing import Any, Callable, Dict, Optional

import attr

from ..models.checksum_description_type import ChecksumDescriptionType
from ..types import UNSET
from ..util.serialization import is_not_none


@attr.s(auto_attribs=True)
class ChecksumDescription:
    """  """

    header_name: str
    type: ChecksumDescriptionType

    def to_dict(self, pick_by_predicate: Optional[Callable[[Any], bool]] = is_not_none) -> Dict[str, Any]:
        header_name = self.header_name
        type = self.type.value

        dct = {
            k: v
            for k, v in {
                "headerName": header_name,
                "type": type,
            }.items()
            if v != UNSET
        }
        if pick_by_predicate is not None:
            dct = {k: v for k, v in dct.items() if pick_by_predicate(v)}
        return dct

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ChecksumDescription":
        header_name = d["headerName"]

        type = ChecksumDescriptionType(d["type"])

        return ChecksumDescription(
            header_name=header_name,
            type=type,
        )
