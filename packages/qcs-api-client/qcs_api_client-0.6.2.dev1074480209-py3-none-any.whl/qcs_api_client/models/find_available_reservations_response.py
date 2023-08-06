from typing import Any, Callable, Dict, List, Optional, Union

import attr

from ..models.available_reservation import AvailableReservation
from ..types import UNSET, Unset
from ..util.serialization import is_not_none


@attr.s(auto_attribs=True)
class FindAvailableReservationsResponse:
    """  """

    available_reservations: List[AvailableReservation]
    next_page_token: Union[Unset, str] = UNSET

    def to_dict(self, pick_by_predicate: Optional[Callable[[Any], bool]] = is_not_none) -> Dict[str, Any]:
        available_reservations = []
        for available_reservations_item_data in self.available_reservations:
            available_reservations_item = available_reservations_item_data.to_dict()

            available_reservations.append(available_reservations_item)

        next_page_token = self.next_page_token

        dct = {
            k: v
            for k, v in {
                "availableReservations": available_reservations,
                "nextPageToken": next_page_token,
            }.items()
            if v != UNSET
        }
        if pick_by_predicate is not None:
            dct = {k: v for k, v in dct.items() if pick_by_predicate(v)}
        return dct

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "FindAvailableReservationsResponse":
        available_reservations = []
        _available_reservations = d["availableReservations"]
        for available_reservations_item_data in _available_reservations:
            available_reservations_item = AvailableReservation.from_dict(available_reservations_item_data)

            available_reservations.append(available_reservations_item)

        next_page_token = d.get("nextPageToken")

        return FindAvailableReservationsResponse(
            available_reservations=available_reservations,
            next_page_token=next_page_token,
        )
