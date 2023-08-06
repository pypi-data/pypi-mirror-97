from typing import Any, Callable, Dict, List, Optional, Union

import attr

from ..models.validation_error import ValidationError
from ..types import UNSET, Unset
from ..util.serialization import is_not_none


@attr.s(auto_attribs=True)
class Error:
    """  """

    code: str
    message: str
    request_id: str
    validation_errors: Union[Unset, List[ValidationError]] = UNSET

    def to_dict(self, pick_by_predicate: Optional[Callable[[Any], bool]] = is_not_none) -> Dict[str, Any]:
        code = self.code
        message = self.message
        request_id = self.request_id
        validation_errors: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.validation_errors, Unset):
            validation_errors = []
            for validation_errors_item_data in self.validation_errors:
                validation_errors_item = validation_errors_item_data.to_dict()

                validation_errors.append(validation_errors_item)

        dct = {
            k: v
            for k, v in {
                "code": code,
                "message": message,
                "requestId": request_id,
                "validationErrors": validation_errors,
            }.items()
            if v != UNSET
        }
        if pick_by_predicate is not None:
            dct = {k: v for k, v in dct.items() if pick_by_predicate(v)}
        return dct

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Error":
        code = d["code"]

        message = d["message"]

        request_id = d["requestId"]

        validation_errors = []
        _validation_errors = d.get("validationErrors")
        for validation_errors_item_data in _validation_errors or []:
            validation_errors_item = ValidationError.from_dict(validation_errors_item_data)

            validation_errors.append(validation_errors_item)

        return Error(
            code=code,
            message=message,
            request_id=request_id,
            validation_errors=validation_errors,
        )
