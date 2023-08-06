from typing import Any, Callable, Dict, List, Optional

import attr

from ..models.client_application import ClientApplication
from ..types import UNSET
from ..util.serialization import is_not_none


@attr.s(auto_attribs=True)
class ListClientApplicationsResponse:
    """  """

    client_applications: List[ClientApplication]

    def to_dict(self, pick_by_predicate: Optional[Callable[[Any], bool]] = is_not_none) -> Dict[str, Any]:
        client_applications = []
        for client_applications_item_data in self.client_applications:
            client_applications_item = client_applications_item_data.to_dict()

            client_applications.append(client_applications_item)

        dct = {
            k: v
            for k, v in {
                "clientApplications": client_applications,
            }.items()
            if v != UNSET
        }
        if pick_by_predicate is not None:
            dct = {k: v for k, v in dct.items() if pick_by_predicate(v)}
        return dct

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ListClientApplicationsResponse":
        client_applications = []
        _client_applications = d["clientApplications"]
        for client_applications_item_data in _client_applications:
            client_applications_item = ClientApplication.from_dict(client_applications_item_data)

            client_applications.append(client_applications_item)

        return ListClientApplicationsResponse(
            client_applications=client_applications,
        )
