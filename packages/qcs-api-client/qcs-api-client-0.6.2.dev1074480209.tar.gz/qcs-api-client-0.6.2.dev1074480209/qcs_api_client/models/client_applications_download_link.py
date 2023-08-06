from typing import Any, Callable, Dict, Optional, Union, cast

import attr

from ..models.checksum_description import ChecksumDescription
from ..types import UNSET, Unset
from ..util.serialization import is_not_none


@attr.s(auto_attribs=True)
class ClientApplicationsDownloadLink:
    """  """

    url: str
    checksum_description: Union[ChecksumDescription, Unset] = UNSET
    platform: Union[Unset, str] = UNSET

    def to_dict(self, pick_by_predicate: Optional[Callable[[Any], bool]] = is_not_none) -> Dict[str, Any]:
        url = self.url
        checksum_description: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.checksum_description, Unset):
            checksum_description = self.checksum_description.to_dict()

        platform = self.platform

        dct = {
            k: v
            for k, v in {
                "url": url,
                "checksumDescription": checksum_description,
                "platform": platform,
            }.items()
            if v != UNSET
        }
        if pick_by_predicate is not None:
            dct = {k: v for k, v in dct.items() if pick_by_predicate(v)}
        return dct

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ClientApplicationsDownloadLink":
        url = d["url"]

        checksum_description: Union[ChecksumDescription, Unset] = UNSET
        _checksum_description = d.get("checksumDescription")
        if _checksum_description is not None and not isinstance(_checksum_description, Unset):
            checksum_description = ChecksumDescription.from_dict(cast(Dict[str, Any], _checksum_description))

        platform = d.get("platform")

        return ClientApplicationsDownloadLink(
            url=url,
            checksum_description=checksum_description,
            platform=platform,
        )
