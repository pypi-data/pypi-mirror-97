from typing import Any, Callable, Dict, List, Optional, Union, cast

import attr

from ..models.translate_native_quil_to_encrypted_binary_response_memory_descriptors import (
    TranslateNativeQuilToEncryptedBinaryResponseMemoryDescriptors,
)
from ..types import UNSET, Unset
from ..util.serialization import is_not_none


@attr.s(auto_attribs=True)
class TranslateNativeQuilToEncryptedBinaryResponse:
    """  """

    program: str
    memory_descriptors: Union[TranslateNativeQuilToEncryptedBinaryResponseMemoryDescriptors, Unset] = UNSET
    ro_sources: Union[Unset, List[List[str]]] = UNSET

    def to_dict(self, pick_by_predicate: Optional[Callable[[Any], bool]] = is_not_none) -> Dict[str, Any]:
        program = self.program
        memory_descriptors: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.memory_descriptors, Unset):
            memory_descriptors = self.memory_descriptors.to_dict()

        ro_sources: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.ro_sources, Unset):
            ro_sources = []
            for ro_sources_item_data in self.ro_sources:
                ro_sources_item = ro_sources_item_data

                ro_sources.append(ro_sources_item)

        dct = {
            k: v
            for k, v in {
                "program": program,
                "memoryDescriptors": memory_descriptors,
                "roSources": ro_sources,
            }.items()
            if v != UNSET
        }
        if pick_by_predicate is not None:
            dct = {k: v for k, v in dct.items() if pick_by_predicate(v)}
        return dct

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "TranslateNativeQuilToEncryptedBinaryResponse":
        program = d["program"]

        memory_descriptors: Union[TranslateNativeQuilToEncryptedBinaryResponseMemoryDescriptors, Unset] = UNSET
        _memory_descriptors = d.get("memoryDescriptors")
        if _memory_descriptors is not None and not isinstance(_memory_descriptors, Unset):
            memory_descriptors = TranslateNativeQuilToEncryptedBinaryResponseMemoryDescriptors.from_dict(
                cast(Dict[str, Any], _memory_descriptors)
            )

        ro_sources = []
        _ro_sources = d.get("roSources")
        for ro_sources_item_data in _ro_sources or []:
            ro_sources_item = cast(List[str], ro_sources_item_data)

            ro_sources.append(ro_sources_item)

        return TranslateNativeQuilToEncryptedBinaryResponse(
            program=program,
            memory_descriptors=memory_descriptors,
            ro_sources=ro_sources,
        )
