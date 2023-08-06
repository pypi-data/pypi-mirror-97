from typing import Any, Callable, Dict, Optional, Union

import attr

from ..types import UNSET, Unset
from ..util.serialization import is_not_none


@attr.s(auto_attribs=True)
class CreateEngagementRequest:
    """  """

    endpoint_id: Union[Unset, str] = UNSET
    quantum_processor_id: Union[Unset, str] = UNSET

    def to_dict(self, pick_by_predicate: Optional[Callable[[Any], bool]] = is_not_none) -> Dict[str, Any]:
        endpoint_id = self.endpoint_id
        quantum_processor_id = self.quantum_processor_id

        dct = {
            k: v
            for k, v in {
                "endpointId": endpoint_id,
                "quantumProcessorId": quantum_processor_id,
            }.items()
            if v != UNSET
        }
        if pick_by_predicate is not None:
            dct = {k: v for k, v in dct.items() if pick_by_predicate(v)}
        return dct

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "CreateEngagementRequest":
        endpoint_id = d.get("endpointId")

        quantum_processor_id = d.get("quantumProcessorId")

        return CreateEngagementRequest(
            endpoint_id=endpoint_id,
            quantum_processor_id=quantum_processor_id,
        )
