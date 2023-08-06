from typing import Any, Callable, Dict, Optional

import attr

from ..types import UNSET
from ..util.serialization import is_not_none


@attr.s(auto_attribs=True)
class Order:
    """A string conforming to order specification described in [Google AIP 132](https://google.aip.dev/132#ordering).

    * Fields are specific to the route in question, but are typically a subset of attributes of the requested resource.
    * May include a comma separated list of many fields.
    * Fields are sorted in *ascending* order unless the field is followed by ` DESC`.

    For example, `quantumProcessorId, startTime DESC`.
    """

    def to_dict(self, pick_by_predicate: Optional[Callable[[Any], bool]] = is_not_none) -> Dict[str, Any]:

        dct = {k: v for k, v in {}.items() if v != UNSET}
        if pick_by_predicate is not None:
            dct = {k: v for k, v in dct.items() if pick_by_predicate(v)}
        return dct

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Order":
        return Order()
