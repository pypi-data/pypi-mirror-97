import datetime
from typing import Any, Callable, Dict, List, Optional, Union, cast

import attr
from dateutil.parser import isoparse
from rfc3339 import rfc3339

from ..types import UNSET, Unset
from ..util.serialization import is_not_none


@attr.s(auto_attribs=True)
class Characteristic:
    """ A measured characteristic of an operation. """

    name: str
    timestamp: datetime.datetime
    value: float
    error: Union[Unset, float] = UNSET
    node_ids: Union[Unset, List[int]] = UNSET
    parameter_values: Union[Unset, List[float]] = UNSET

    def to_dict(self, pick_by_predicate: Optional[Callable[[Any], bool]] = is_not_none) -> Dict[str, Any]:
        name = self.name
        assert self.timestamp.tzinfo is not None, "Datetime must have timezone information"
        timestamp = rfc3339(self.timestamp)

        value = self.value
        error = self.error
        node_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.node_ids, Unset):
            node_ids = self.node_ids

        parameter_values: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.parameter_values, Unset):
            parameter_values = self.parameter_values

        dct = {
            k: v
            for k, v in {
                "name": name,
                "timestamp": timestamp,
                "value": value,
                "error": error,
                "node_ids": node_ids,
                "parameter_values": parameter_values,
            }.items()
            if v != UNSET
        }
        if pick_by_predicate is not None:
            dct = {k: v for k, v in dct.items() if pick_by_predicate(v)}
        return dct

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Characteristic":
        name = d["name"]

        timestamp = isoparse(d["timestamp"])

        value = d["value"]

        error = d.get("error")

        node_ids = cast(List[int], d.get("node_ids"))

        parameter_values = cast(List[float], d.get("parameter_values"))

        return Characteristic(
            name=name,
            timestamp=timestamp,
            value=value,
            error=error,
            node_ids=node_ids,
            parameter_values=parameter_values,
        )
