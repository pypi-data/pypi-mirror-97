from typing import Any, Callable, Dict, Optional, Union

import attr

from ..models.engagement_credentials import EngagementCredentials
from ..types import UNSET, Unset
from ..util.serialization import is_not_none


@attr.s(auto_attribs=True)
class EngagementWithCredentials:
    """ An engagement is the authorization of a user to execute work on a Quantum Processor Endpoint. """

    address: str
    credentials: EngagementCredentials
    endpoint_id: str
    expires_at: str
    quantum_processor_id: str
    user_id: str
    minimum_priority: Union[Unset, int] = UNSET

    def to_dict(self, pick_by_predicate: Optional[Callable[[Any], bool]] = is_not_none) -> Dict[str, Any]:
        address = self.address
        credentials = self.credentials.to_dict()

        endpoint_id = self.endpoint_id
        expires_at = self.expires_at
        quantum_processor_id = self.quantum_processor_id
        user_id = self.user_id
        minimum_priority = self.minimum_priority

        dct = {
            k: v
            for k, v in {
                "address": address,
                "credentials": credentials,
                "endpointId": endpoint_id,
                "expiresAt": expires_at,
                "quantumProcessorId": quantum_processor_id,
                "userId": user_id,
                "minimumPriority": minimum_priority,
            }.items()
            if v != UNSET
        }
        if pick_by_predicate is not None:
            dct = {k: v for k, v in dct.items() if pick_by_predicate(v)}
        return dct

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EngagementWithCredentials":
        address = d["address"]

        credentials = EngagementCredentials.from_dict(d["credentials"])

        endpoint_id = d["endpointId"]

        expires_at = d["expiresAt"]

        quantum_processor_id = d["quantumProcessorId"]

        user_id = d["userId"]

        minimum_priority = d.get("minimumPriority")

        return EngagementWithCredentials(
            address=address,
            credentials=credentials,
            endpoint_id=endpoint_id,
            expires_at=expires_at,
            quantum_processor_id=quantum_processor_id,
            user_id=user_id,
            minimum_priority=minimum_priority,
        )
