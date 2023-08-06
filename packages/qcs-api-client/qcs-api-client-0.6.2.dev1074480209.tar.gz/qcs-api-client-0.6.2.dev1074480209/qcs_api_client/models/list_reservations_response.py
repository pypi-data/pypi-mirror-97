from typing import Any, Callable, Dict, List, Optional

import attr

from ..models.reservation import Reservation
from ..types import UNSET
from ..util.serialization import is_not_none


@attr.s(auto_attribs=True)
class ListReservationsResponse:
    """  """

    next_page_token: str
    reservations: List[Reservation]

    def to_dict(self, pick_by_predicate: Optional[Callable[[Any], bool]] = is_not_none) -> Dict[str, Any]:
        next_page_token = self.next_page_token
        reservations = []
        for reservations_item_data in self.reservations:
            reservations_item = reservations_item_data.to_dict()

            reservations.append(reservations_item)

        dct = {
            k: v
            for k, v in {
                "nextPageToken": next_page_token,
                "reservations": reservations,
            }.items()
            if v != UNSET
        }
        if pick_by_predicate is not None:
            dct = {k: v for k, v in dct.items() if pick_by_predicate(v)}
        return dct

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ListReservationsResponse":
        next_page_token = d["nextPageToken"]

        reservations = []
        _reservations = d["reservations"]
        for reservations_item_data in _reservations:
            reservations_item = Reservation.from_dict(reservations_item_data)

            reservations.append(reservations_item)

        return ListReservationsResponse(
            next_page_token=next_page_token,
            reservations=reservations,
        )
