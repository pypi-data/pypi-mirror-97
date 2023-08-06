import datetime
from typing import Any, Callable, Dict, Optional, Union, cast

import attr
from dateutil.parser import isoparse
from rfc3339 import rfc3339

from ..types import UNSET, Unset
from ..util.serialization import is_not_none


@attr.s(auto_attribs=True)
class Reservation:
    """  """

    created_time: datetime.datetime
    end_time: datetime.datetime
    id: int
    price: int
    quantum_processor_id: str
    start_time: datetime.datetime
    user_id: str
    cancelled: Union[Unset, bool] = UNSET
    notes: Union[Unset, str] = UNSET
    updated_time: Union[Unset, datetime.datetime] = UNSET

    def to_dict(self, pick_by_predicate: Optional[Callable[[Any], bool]] = is_not_none) -> Dict[str, Any]:
        assert self.created_time.tzinfo is not None, "Datetime must have timezone information"
        created_time = rfc3339(self.created_time)

        assert self.end_time.tzinfo is not None, "Datetime must have timezone information"
        end_time = rfc3339(self.end_time)

        id = self.id
        price = self.price
        quantum_processor_id = self.quantum_processor_id
        assert self.start_time.tzinfo is not None, "Datetime must have timezone information"
        start_time = rfc3339(self.start_time)

        user_id = self.user_id
        cancelled = self.cancelled
        notes = self.notes
        updated_time: Union[Unset, str] = UNSET
        if not isinstance(self.updated_time, Unset):
            assert self.updated_time.tzinfo is not None, "Datetime must have timezone information"
            updated_time = rfc3339(self.updated_time)

        dct = {
            k: v
            for k, v in {
                "createdTime": created_time,
                "endTime": end_time,
                "id": id,
                "price": price,
                "quantumProcessorId": quantum_processor_id,
                "startTime": start_time,
                "userId": user_id,
                "cancelled": cancelled,
                "notes": notes,
                "updatedTime": updated_time,
            }.items()
            if v != UNSET
        }
        if pick_by_predicate is not None:
            dct = {k: v for k, v in dct.items() if pick_by_predicate(v)}
        return dct

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Reservation":
        created_time = isoparse(d["createdTime"])

        end_time = isoparse(d["endTime"])

        id = d["id"]

        price = d["price"]

        quantum_processor_id = d["quantumProcessorId"]

        start_time = isoparse(d["startTime"])

        user_id = d["userId"]

        cancelled = d.get("cancelled")

        notes = d.get("notes")

        updated_time = None
        if d.get("updatedTime") is not None:
            updated_time = isoparse(cast(str, d.get("updatedTime")))

        return Reservation(
            created_time=created_time,
            end_time=end_time,
            id=id,
            price=price,
            quantum_processor_id=quantum_processor_id,
            start_time=start_time,
            user_id=user_id,
            cancelled=cancelled,
            notes=notes,
            updated_time=updated_time,
        )
