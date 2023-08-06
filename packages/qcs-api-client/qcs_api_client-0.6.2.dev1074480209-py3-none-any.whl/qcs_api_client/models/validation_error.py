from typing import Any, Callable, Dict, List, Optional, Union, cast

import attr

from ..models.validation_error_in import ValidationErrorIn
from ..types import UNSET, Unset
from ..util.serialization import is_not_none


@attr.s(auto_attribs=True)
class ValidationError:
    """  """

    in_: ValidationErrorIn
    message: str
    path: Union[Unset, List[str]] = UNSET

    def to_dict(self, pick_by_predicate: Optional[Callable[[Any], bool]] = is_not_none) -> Dict[str, Any]:
        in_ = self.in_.value

        message = self.message
        path: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.path, Unset):
            path = self.path

        dct = {
            k: v
            for k, v in {
                "in": in_,
                "message": message,
                "path": path,
            }.items()
            if v != UNSET
        }
        if pick_by_predicate is not None:
            dct = {k: v for k, v in dct.items() if pick_by_predicate(v)}
        return dct

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ValidationError":
        in_ = ValidationErrorIn(d["in"])

        message = d["message"]

        path = cast(List[str], d.get("path"))

        return ValidationError(
            in_=in_,
            message=message,
            path=path,
        )
