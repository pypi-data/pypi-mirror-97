from typing import Any, Callable, Dict, List, Optional, Union

import attr

from ..models.client_applications_download_link import ClientApplicationsDownloadLink
from ..types import UNSET, Unset
from ..util.serialization import is_not_none


@attr.s(auto_attribs=True)
class ClientApplication:
    """  """

    latest_version: str
    name: str
    supported: bool
    details_uri: Union[Unset, str] = UNSET
    links: Union[Unset, List[ClientApplicationsDownloadLink]] = UNSET
    minimum_version: Union[Unset, str] = UNSET

    def to_dict(self, pick_by_predicate: Optional[Callable[[Any], bool]] = is_not_none) -> Dict[str, Any]:
        latest_version = self.latest_version
        name = self.name
        supported = self.supported
        details_uri = self.details_uri
        links: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.links, Unset):
            links = []
            for links_item_data in self.links:
                links_item = links_item_data.to_dict()

                links.append(links_item)

        minimum_version = self.minimum_version

        dct = {
            k: v
            for k, v in {
                "latestVersion": latest_version,
                "name": name,
                "supported": supported,
                "detailsUri": details_uri,
                "links": links,
                "minimumVersion": minimum_version,
            }.items()
            if v != UNSET
        }
        if pick_by_predicate is not None:
            dct = {k: v for k, v in dct.items() if pick_by_predicate(v)}
        return dct

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ClientApplication":
        latest_version = d["latestVersion"]

        name = d["name"]

        supported = d["supported"]

        details_uri = d.get("detailsUri")

        links = []
        _links = d.get("links")
        for links_item_data in _links or []:
            links_item = ClientApplicationsDownloadLink.from_dict(links_item_data)

            links.append(links_item)

        minimum_version = d.get("minimumVersion")

        return ClientApplication(
            latest_version=latest_version,
            name=name,
            supported=supported,
            details_uri=details_uri,
            links=links,
            minimum_version=minimum_version,
        )
