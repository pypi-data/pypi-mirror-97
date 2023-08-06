from typing import Any, Callable, Dict, List, Optional, Union

import attr

from ..models.characteristic import Characteristic
from ..models.operation_site import OperationSite
from ..models.parameter import Parameter
from ..types import UNSET, Unset
from ..util.serialization import is_not_none


@attr.s(auto_attribs=True)
class Operation:
    """ An operation, with its sites and site-independent characteristics. """

    characteristics: List[Characteristic]
    name: str
    parameters: List[Parameter]
    sites: List[OperationSite]
    node_count: Union[Unset, int] = UNSET

    def to_dict(self, pick_by_predicate: Optional[Callable[[Any], bool]] = is_not_none) -> Dict[str, Any]:
        characteristics = []
        for characteristics_item_data in self.characteristics:
            characteristics_item = characteristics_item_data.to_dict()

            characteristics.append(characteristics_item)

        name = self.name
        parameters = []
        for parameters_item_data in self.parameters:
            parameters_item = parameters_item_data.to_dict()

            parameters.append(parameters_item)

        sites = []
        for sites_item_data in self.sites:
            sites_item = sites_item_data.to_dict()

            sites.append(sites_item)

        node_count = self.node_count

        dct = {
            k: v
            for k, v in {
                "characteristics": characteristics,
                "name": name,
                "parameters": parameters,
                "sites": sites,
                "node_count": node_count,
            }.items()
            if v != UNSET
        }
        if pick_by_predicate is not None:
            dct = {k: v for k, v in dct.items() if pick_by_predicate(v)}
        return dct

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Operation":
        characteristics = []
        _characteristics = d["characteristics"]
        for characteristics_item_data in _characteristics:
            characteristics_item = Characteristic.from_dict(characteristics_item_data)

            characteristics.append(characteristics_item)

        name = d["name"]

        parameters = []
        _parameters = d["parameters"]
        for parameters_item_data in _parameters:
            parameters_item = Parameter.from_dict(parameters_item_data)

            parameters.append(parameters_item)

        sites = []
        _sites = d["sites"]
        for sites_item_data in _sites:
            sites_item = OperationSite.from_dict(sites_item_data)

            sites.append(sites_item)

        node_count = d.get("node_count")

        return Operation(
            characteristics=characteristics,
            name=name,
            parameters=parameters,
            sites=sites,
            node_count=node_count,
        )
