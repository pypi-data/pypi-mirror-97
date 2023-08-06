from typing import Any, Callable, Dict, List, Optional

import attr

from ..models.architecture import Architecture
from ..models.operation import Operation
from ..types import UNSET
from ..util.serialization import is_not_none


@attr.s(auto_attribs=True)
class InstructionSetArchitecture:
    """The native instruction set architecture of a quantum processor, annotated with characteristics.

    The operations described by the `instructions` field are named by their QUIL instruction name,
    while the operation described by the `benchmarks` field are named by their benchmark routine
    and are a future extension point that will be populated in future iterations.

    The characteristics that annotate both instructions and benchmarks assist the user to generate
    the best native QUIL program for a desired task, and so are provided as part of the native ISA."""

    architecture: Architecture
    benchmarks: List[Operation]
    instructions: List[Operation]
    name: str

    def to_dict(self, pick_by_predicate: Optional[Callable[[Any], bool]] = is_not_none) -> Dict[str, Any]:
        architecture = self.architecture.to_dict()

        benchmarks = []
        for benchmarks_item_data in self.benchmarks:
            benchmarks_item = benchmarks_item_data.to_dict()

            benchmarks.append(benchmarks_item)

        instructions = []
        for instructions_item_data in self.instructions:
            instructions_item = instructions_item_data.to_dict()

            instructions.append(instructions_item)

        name = self.name

        dct = {
            k: v
            for k, v in {
                "architecture": architecture,
                "benchmarks": benchmarks,
                "instructions": instructions,
                "name": name,
            }.items()
            if v != UNSET
        }
        if pick_by_predicate is not None:
            dct = {k: v for k, v in dct.items() if pick_by_predicate(v)}
        return dct

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "InstructionSetArchitecture":
        architecture = Architecture.from_dict(d["architecture"])

        benchmarks = []
        _benchmarks = d["benchmarks"]
        for benchmarks_item_data in _benchmarks:
            benchmarks_item = Operation.from_dict(benchmarks_item_data)

            benchmarks.append(benchmarks_item)

        instructions = []
        _instructions = d["instructions"]
        for instructions_item_data in _instructions:
            instructions_item = Operation.from_dict(instructions_item_data)

            instructions.append(instructions_item)

        name = d["name"]

        return InstructionSetArchitecture(
            architecture=architecture,
            benchmarks=benchmarks,
            instructions=instructions,
            name=name,
        )
