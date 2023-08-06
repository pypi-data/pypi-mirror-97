import datetime
from typing import Any, Callable, Dict, Optional

import attr
from dateutil.parser import isoparse
from rfc3339 import rfc3339

from ..types import UNSET
from ..util.serialization import is_not_none


@attr.s(auto_attribs=True)
class AvailableReservation:
    """  """

    duration: str
    end_time: datetime.datetime
    price: int
    quantum_processor_id: str
    start_time: datetime.datetime

    def to_dict(self, pick_by_predicate: Optional[Callable[[Any], bool]] = is_not_none) -> Dict[str, Any]:
        duration = self.duration
        assert self.end_time.tzinfo is not None, "Datetime must have timezone information"
        end_time = rfc3339(self.end_time)

        price = self.price
        quantum_processor_id = self.quantum_processor_id
        assert self.start_time.tzinfo is not None, "Datetime must have timezone information"
        start_time = rfc3339(self.start_time)

        dct = {
            k: v
            for k, v in {
                "duration": duration,
                "endTime": end_time,
                "price": price,
                "quantumProcessorId": quantum_processor_id,
                "startTime": start_time,
            }.items()
            if v != UNSET
        }
        if pick_by_predicate is not None:
            dct = {k: v for k, v in dct.items() if pick_by_predicate(v)}
        return dct

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AvailableReservation":
        duration = d["duration"]

        end_time = isoparse(d["endTime"])

        price = d["price"]

        quantum_processor_id = d["quantumProcessorId"]

        start_time = isoparse(d["startTime"])

        return AvailableReservation(
            duration=duration,
            end_time=end_time,
            price=price,
            quantum_processor_id=quantum_processor_id,
            start_time=start_time,
        )
