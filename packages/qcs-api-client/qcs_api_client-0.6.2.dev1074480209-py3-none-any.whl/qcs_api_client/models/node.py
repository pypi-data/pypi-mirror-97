from typing import Any, Callable, Dict, Optional

import attr

from ..types import UNSET
from ..util.serialization import is_not_none


@attr.s(auto_attribs=True)
class Node:
    """A logical node in the quantum processor's architecture.

    The existence of a node in the ISA `Architecture` does not necessarily mean that a given 1Q
    operation will be available on the node. This information is conveyed by the presence of the
    specific `node_id` in instances of `Instruction`."""

    node_id: int

    def to_dict(self, pick_by_predicate: Optional[Callable[[Any], bool]] = is_not_none) -> Dict[str, Any]:
        node_id = self.node_id

        dct = {
            k: v
            for k, v in {
                "node_id": node_id,
            }.items()
            if v != UNSET
        }
        if pick_by_predicate is not None:
            dct = {k: v for k, v in dct.items() if pick_by_predicate(v)}
        return dct

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Node":
        node_id = d["node_id"]

        return Node(
            node_id=node_id,
        )
