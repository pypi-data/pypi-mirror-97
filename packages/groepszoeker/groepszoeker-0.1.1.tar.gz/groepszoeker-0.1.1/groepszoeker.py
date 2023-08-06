# Copyright 2021 Graham Binns <hello@gmb.dev>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Utilities to find a sub population to match a given input value."""

import enum
from decimal import Decimal
from typing import (
    Any,
    Iterable,
    Union,
)
from uuid import uuid4


__all__ = [
    "find_population",
]


Numeric = Union[float, int, Decimal]


class TotalBoundsCheckStatus(enum.Enum):
    """An enum to indicate whether a total is in or out of bounds."""

    at_outer_limit = enum.auto()
    bounds_not_reached = enum.auto()
    in_bounds = enum.auto()
    out_of_bounds = enum.auto()


class SearchableItem:
    """An item with a value, which can be searched for as part of a sub-pop."""

    def __init__(self, *, id: Any = None, value: Numeric = 0):
        """Create a new SearchableItem."""
        self.id = id or uuid4()
        self.value = value

    def __repr__(self):
        """Return a string representation of a SearchableItem."""
        return f"{self.id=}: {self.value=}"


class ClassifiedItemCollection:
    """A class to hold a population of SearchableItems, classified into segments.

    The segments are units, tens, hundreds, thousands, ten thousands, hundred
    thousands, and millions.

    Items are classified on their absolute value.
    """

    def __init__(self, *, items: Iterable[SearchableItem]):
        """Create a new ClassifiedItemCollection."""
        self.units = set(item for item in items if abs(item.value) < 10)
        self.tens = set(item for item in items if 10 < abs(item.value) < 100)
        self.hundreds = set(
            item for item in items if 99 < abs(item.value) < 1000
        )
        self.thousands = set(
            item for item in items if 999 < abs(item.value) < 10000
        )
        self.ten_thousands = set(
            item for item in items if 9999 < abs(item.value) < 100000
        )
        self.hundred_thousands = set(
            item for item in items if 99999 < abs(item.value) < 1000000
        )
        self.millions = set(item for item in items if 999999 < abs(item.value))


class SubPopulation:
    """A collection of items representing a subpopulation of another population."""

    def __init__(
        self,
        *,
        total_value: Numeric = 0,
        matched_items: set = None,
        unmatched_items: set = None,
        metadata: dict = None,
    ):
        """Create a new SubPopulation."""
        self.total_value = total_value
        self.matched_items = matched_items.copy() or set()
        self.unmatched_items = unmatched_items.copy() or set()
        self.metadata = metadata or {}

    def __repr__(self):
        """Return a string representation of this SubPopulation."""
        return (
            f"{self.total_value=} {self.matched_items=} {self.unmatched_items=}"
        )


def find_population(
    target: Numeric,
    tolerance: Numeric,
    items: Iterable[SearchableItem],
    max_search_attempts: Union[int, None] = None,
    return_alternatives: bool = False,
):
    """Find sub-populations within `items` which have total value of `target`.

    Will return the largest (i.e. having-most-items) sub-population where the
    sum of values of `items` is equal to `target` +/- `tolerance`.

    :param target: The value for which we're trying to find a sub-population.
        A group of items is considered a valid sub-population if the sum of
        their values is equal to this target, within `tolerance`.
    :param tolerance: A positive value indicating by how much to allow a
        current value to differ from the target value whilst still
        considering it valid.
    :param items: An iterable of SearchableItem, or at least
        SearchableItem-like objects, in which we want to try to find sub
        populations.
    :param max_search_attempts: The maximum number of times to loop through
        items, attempting to find a sub-population, before giving up. If
        None, `find_population()` will exhaustively search until it's got no
        options left.
        This is a useful parameter to try and keep the function from ending up
        being O(N!).
    :param return_alternatives: If True, return a tuple of
        (largest_sub_population, other_sub_populations), where
        other_sub_populations is a list of SubPopulations which were found
        when searching, but which weren't the largest.
    :return: The largest valid sub-population. If `return_alternatives` is
        True, return a tuple of (largest_sub_pop, alternative_sub_pops). If
        no sub-population is found, return None.
    """
    items = set(items)
    lower_bound = target - tolerance
    upper_bound = target + tolerance

    # If the sum of all the values is within tolerance, we can return the whole
    # set.
    sum_of_all_values = sum([item.value for item in items])
    if lower_bound <= sum_of_all_values <= upper_bound:
        return SubPopulation(
            total_value=sum_of_all_values,
            matched_items=items,
        )

    possible_sub_pops = []
    window_start = 0

    # Sliding window. Add items sequentially. If we go over the upper bound,
    # shift the window over one and start again.
    while window_start < len(items) and (
        max_search_attempts is None or window_start < max_search_attempts
    ):
        possible_sub_pops += find_possible_sub_populations(
            items, window_start, target, tolerance
        )
        window_start += 1

    if possible_sub_pops:
        possible_sub_pops = sorted(
            possible_sub_pops,
            key=lambda sub_pop: len(sub_pop.matched_items),
            reverse=True,
        )
        largest_sub_pop = possible_sub_pops[0]
        if return_alternatives:
            return largest_sub_pop, possible_sub_pops[1:]
        return largest_sub_pop

    if return_alternatives:
        return None, None
    return None


def check_bounds(
    total: Numeric, target: Numeric, tolerance: Numeric
) -> TotalBoundsCheckStatus:
    """Check whether a total is in or out of bounds.

    :param total: The total to bounds-check.
    :param target: The value to check total against.
    :param tolerance: The amount +/- `target` within which `total` will be
        accepted.

    >>> check_bounds(total=100, target=110, tolerance=15)
    <TotalBoundsCheckStatus.in_bounds: 3>
    """
    lower_bound = target - tolerance
    upper_bound = target + tolerance

    if target < 0:
        # Deal with -ve targets.
        if total < lower_bound:
            return TotalBoundsCheckStatus.out_of_bounds
        if total == lower_bound:
            return TotalBoundsCheckStatus.at_outer_limit
        if lower_bound < total <= upper_bound:
            return TotalBoundsCheckStatus.in_bounds
        else:
            return TotalBoundsCheckStatus.bounds_not_reached

    if total > upper_bound:
        return TotalBoundsCheckStatus.out_of_bounds
    if total == upper_bound:
        return TotalBoundsCheckStatus.at_outer_limit
    if lower_bound <= total < upper_bound:
        return TotalBoundsCheckStatus.in_bounds
    else:
        return TotalBoundsCheckStatus.bounds_not_reached


def find_possible_sub_populations(items, window_start, target, tolerance):
    """Loop over items and find possible sub populations.

    Return any possible sub populations found, or an empty list if none are
    found before the loop needs to exit.
    """
    sorted_items = sorted(items, key=lambda item: item.value)
    result_collection = set()
    current_total = 0
    possible_sub_pops = []

    for item in sorted_items[window_start:]:
        new_total = current_total + item.value
        bounds_check_result = check_bounds(new_total, target, tolerance)

        if bounds_check_result in (
            TotalBoundsCheckStatus.in_bounds,
            TotalBoundsCheckStatus.bounds_not_reached,
            TotalBoundsCheckStatus.at_outer_limit,
        ):
            # If we're below the lower bound or between the bounds, we're
            # fine.
            current_total = new_total
            result_collection.add(item)

        if bounds_check_result in (
            TotalBoundsCheckStatus.in_bounds,
            TotalBoundsCheckStatus.at_outer_limit,
        ):
            # We're within the upper and lower bounds, so we can consider
            # this a valid sub-pop.
            possible_sub_pops.append(
                SubPopulation(
                    matched_items=result_collection,
                    unmatched_items=items.difference(result_collection),
                    total_value=sum([item.value for item in result_collection]),
                    metadata={
                        "attempts_taken": window_start + 1,
                    },
                )
            )
        if bounds_check_result == TotalBoundsCheckStatus.out_of_bounds:
            # Erk. Too far. Bail out so that the callsite can call this
            # function with a new window_start.
            break

    return possible_sub_pops
