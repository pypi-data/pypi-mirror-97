import datetime
from typing import Any, Callable, Dict, Optional, Union

import attr
from dateutil.parser import isoparse
from rfc3339 import rfc3339

from ..types import UNSET, Unset
from ..util.serialization import is_not_none


@attr.s(auto_attribs=True)
class CreateReservationRequest:
    """  """

    end_time: datetime.datetime
    quantum_processor_id: str
    start_time: datetime.datetime
    notes: Union[Unset, str] = UNSET

    def to_dict(self, pick_by_predicate: Optional[Callable[[Any], bool]] = is_not_none) -> Dict[str, Any]:
        assert self.end_time.tzinfo is not None, "Datetime must have timezone information"
        end_time = rfc3339(self.end_time)

        quantum_processor_id = self.quantum_processor_id
        assert self.start_time.tzinfo is not None, "Datetime must have timezone information"
        start_time = rfc3339(self.start_time)

        notes = self.notes

        dct = {
            k: v
            for k, v in {
                "endTime": end_time,
                "quantumProcessorId": quantum_processor_id,
                "startTime": start_time,
                "notes": notes,
            }.items()
            if v != UNSET
        }
        if pick_by_predicate is not None:
            dct = {k: v for k, v in dct.items() if pick_by_predicate(v)}
        return dct

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "CreateReservationRequest":
        end_time = isoparse(d["endTime"])

        quantum_processor_id = d["quantumProcessorId"]

        start_time = isoparse(d["startTime"])

        notes = d.get("notes")

        return CreateReservationRequest(
            end_time=end_time,
            quantum_processor_id=quantum_processor_id,
            start_time=start_time,
            notes=notes,
        )
