from typing import Any, Callable, Dict, List, Optional, Union

import attr

from ..models.endpoint import Endpoint
from ..types import UNSET, Unset
from ..util.serialization import is_not_none


@attr.s(auto_attribs=True)
class ListEndpointsResponse:
    """  """

    endpoints: List[Endpoint]
    next_page_token: Union[Unset, str] = UNSET

    def to_dict(self, pick_by_predicate: Optional[Callable[[Any], bool]] = is_not_none) -> Dict[str, Any]:
        endpoints = []
        for endpoints_item_data in self.endpoints:
            endpoints_item = endpoints_item_data.to_dict()

            endpoints.append(endpoints_item)

        next_page_token = self.next_page_token

        dct = {
            k: v
            for k, v in {
                "endpoints": endpoints,
                "nextPageToken": next_page_token,
            }.items()
            if v != UNSET
        }
        if pick_by_predicate is not None:
            dct = {k: v for k, v in dct.items() if pick_by_predicate(v)}
        return dct

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ListEndpointsResponse":
        endpoints = []
        _endpoints = d["endpoints"]
        for endpoints_item_data in _endpoints:
            endpoints_item = Endpoint.from_dict(endpoints_item_data)

            endpoints.append(endpoints_item)

        next_page_token = d.get("nextPageToken")

        return ListEndpointsResponse(
            endpoints=endpoints,
            next_page_token=next_page_token,
        )
