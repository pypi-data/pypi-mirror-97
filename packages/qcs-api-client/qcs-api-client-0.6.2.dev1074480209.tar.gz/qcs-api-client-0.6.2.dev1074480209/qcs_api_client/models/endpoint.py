from typing import Any, Callable, Dict, Optional

import attr

from ..types import UNSET
from ..util.serialization import is_not_none


@attr.s(auto_attribs=True)
class Endpoint:
    """ An Endpoint is the entry point for remote access to a QuantumProcessor. """

    address: str
    healthy: bool
    id: str
    mock: bool
    quantum_processor_id: str

    def to_dict(self, pick_by_predicate: Optional[Callable[[Any], bool]] = is_not_none) -> Dict[str, Any]:
        address = self.address
        healthy = self.healthy
        id = self.id
        mock = self.mock
        quantum_processor_id = self.quantum_processor_id

        dct = {
            k: v
            for k, v in {
                "address": address,
                "healthy": healthy,
                "id": id,
                "mock": mock,
                "quantumProcessorId": quantum_processor_id,
            }.items()
            if v != UNSET
        }
        if pick_by_predicate is not None:
            dct = {k: v for k, v in dct.items() if pick_by_predicate(v)}
        return dct

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Endpoint":
        address = d["address"]

        healthy = d["healthy"]

        id = d["id"]

        mock = d["mock"]

        quantum_processor_id = d["quantumProcessorId"]

        return Endpoint(
            address=address,
            healthy=healthy,
            id=id,
            mock=mock,
            quantum_processor_id=quantum_processor_id,
        )
