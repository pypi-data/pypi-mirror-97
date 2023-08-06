from typing import Any, Callable, Dict, Optional, Union

import attr

from ..types import UNSET, Unset
from ..util.serialization import is_not_none


@attr.s(auto_attribs=True)
class TranslateNativeQuilToEncryptedBinaryRequest:
    """  """

    num_shots: int
    quil: str
    settings_timestamp: Union[Unset, str] = UNSET

    def to_dict(self, pick_by_predicate: Optional[Callable[[Any], bool]] = is_not_none) -> Dict[str, Any]:
        num_shots = self.num_shots
        quil = self.quil
        settings_timestamp = self.settings_timestamp

        dct = {
            k: v
            for k, v in {
                "numShots": num_shots,
                "quil": quil,
                "settingsTimestamp": settings_timestamp,
            }.items()
            if v != UNSET
        }
        if pick_by_predicate is not None:
            dct = {k: v for k, v in dct.items() if pick_by_predicate(v)}
        return dct

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "TranslateNativeQuilToEncryptedBinaryRequest":
        num_shots = d["numShots"]

        quil = d["quil"]

        settings_timestamp = d.get("settingsTimestamp")

        return TranslateNativeQuilToEncryptedBinaryRequest(
            num_shots=num_shots,
            quil=quil,
            settings_timestamp=settings_timestamp,
        )
