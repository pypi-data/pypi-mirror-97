from typing import Any, Callable, Dict, Optional

import attr

from ..types import UNSET
from ..util.serialization import is_not_none


@attr.s(auto_attribs=True)
class EngagementCredentials:
    """Credentials are the ZeroMQ CURVE Keys used to encrypt the connection with the Quantum Processor
    Endpoint."""

    client_public: str
    client_secret: str
    server_public: str

    def to_dict(self, pick_by_predicate: Optional[Callable[[Any], bool]] = is_not_none) -> Dict[str, Any]:
        client_public = self.client_public
        client_secret = self.client_secret
        server_public = self.server_public

        dct = {
            k: v
            for k, v in {
                "clientPublic": client_public,
                "clientSecret": client_secret,
                "serverPublic": server_public,
            }.items()
            if v != UNSET
        }
        if pick_by_predicate is not None:
            dct = {k: v for k, v in dct.items() if pick_by_predicate(v)}
        return dct

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EngagementCredentials":
        client_public = d["clientPublic"]

        client_secret = d["clientSecret"]

        server_public = d["serverPublic"]

        return EngagementCredentials(
            client_public=client_public,
            client_secret=client_secret,
            server_public=server_public,
        )
