from typing import Any, Callable, Dict, Optional

import attr

from ..types import UNSET
from ..util.serialization import is_not_none


@attr.s(auto_attribs=True)
class Filter:
    """A string conforming to a *limited* set of the filtering operations described in [Google AIP 160](https://google.aip.dev/160).

    * Expressions are always of the form `{field} {operator} {value}` and may be grouped with `()` and joined with `AND` or `OR`.
    * Fields are specific to the route in question, but are typically a subset of attributes of the requested resource.
    * Operators are limited to `=`, `>`, `>=`, `<`, `<=`, and `!=`.
    * Values may take the following forms:
      * `true` or `false` for boolean fields
      * a number
      * a string (include surrounding `"`s),
      * a duration string (include surrounding `"`s). Valid time units are "ns", "us" (or "µs"), "ms", "s", "m", "h".
      * a date string (include surrounding `"`s). Should be formatted [RFC3339 5.6](https://tools.ietf.org/html/rfc3339#section-5.6).

    For example, `startTime >= "2020-06-24T22:00:00.000Z" OR (duration >= "15m" AND endTime < "2020-06-24T22:00:00.000Z")`.
    """

    def to_dict(self, pick_by_predicate: Optional[Callable[[Any], bool]] = is_not_none) -> Dict[str, Any]:

        dct = {k: v for k, v in {}.items() if v != UNSET}
        if pick_by_predicate is not None:
            dct = {k: v for k, v in dct.items() if pick_by_predicate(v)}
        return dct

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Filter":
        return Filter()
