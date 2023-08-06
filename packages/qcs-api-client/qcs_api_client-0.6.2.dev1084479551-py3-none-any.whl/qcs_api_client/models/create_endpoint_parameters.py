from typing import Any, Callable, Dict, Optional

import attr

from ..types import UNSET
from ..util.serialization import is_not_none


@attr.s(auto_attribs=True)
class CreateEndpointParameters:
    """ A publicly available set of parameters for defining an endpoint. """

    quantum_processor_id: str

    def to_dict(self, pick_by_predicate: Optional[Callable[[Any], bool]] = is_not_none) -> Dict[str, Any]:
        quantum_processor_id = self.quantum_processor_id

        dct = {
            k: v
            for k, v in {
                "quantumProcessorId": quantum_processor_id,
            }.items()
            if v != UNSET
        }
        if pick_by_predicate is not None:
            dct = {k: v for k, v in dct.items() if pick_by_predicate(v)}
        return dct

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "CreateEndpointParameters":
        quantum_processor_id = d["quantumProcessorId"]

        return CreateEndpointParameters(
            quantum_processor_id=quantum_processor_id,
        )
