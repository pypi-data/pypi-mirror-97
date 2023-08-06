from typing import Any, Callable, Dict, List, Optional, Union

import attr

from ..models.quantum_processor import QuantumProcessor
from ..types import UNSET, Unset
from ..util.serialization import is_not_none


@attr.s(auto_attribs=True)
class ListQuantumProcessorsResponse:
    """  """

    quantum_processors: List[QuantumProcessor]
    next_page_token: Union[Unset, str] = UNSET

    def to_dict(self, pick_by_predicate: Optional[Callable[[Any], bool]] = is_not_none) -> Dict[str, Any]:
        quantum_processors = []
        for quantum_processors_item_data in self.quantum_processors:
            quantum_processors_item = quantum_processors_item_data.to_dict()

            quantum_processors.append(quantum_processors_item)

        next_page_token = self.next_page_token

        dct = {
            k: v
            for k, v in {
                "quantumProcessors": quantum_processors,
                "nextPageToken": next_page_token,
            }.items()
            if v != UNSET
        }
        if pick_by_predicate is not None:
            dct = {k: v for k, v in dct.items() if pick_by_predicate(v)}
        return dct

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ListQuantumProcessorsResponse":
        quantum_processors = []
        _quantum_processors = d["quantumProcessors"]
        for quantum_processors_item_data in _quantum_processors:
            quantum_processors_item = QuantumProcessor.from_dict(quantum_processors_item_data)

            quantum_processors.append(quantum_processors_item)

        next_page_token = d.get("nextPageToken")

        return ListQuantumProcessorsResponse(
            quantum_processors=quantum_processors,
            next_page_token=next_page_token,
        )
