import json
from pathlib import Path
from typing import List

from ndl_tools import (
    NoSortListSorter,
    FloatRoundNormalizer,
    ListLastComponentSelector,
    Sorter,
    DefaultListSorter,
    BaseListSorter,
    SELECTORS,
)
from ndl_tools.list_sorter import NotSortedError
from ndl_tools.sorter import SortedList, SortedMapping


def test_sorted_iterable():
    d = [4, 3, 1, 2]
    s = SortedList(d, Path())
    assert s == [1, 2, 3, 4]


def test_sorted_mapping():
    d = {"b": 2, "a": 1}
    sorted_dict = SortedMapping(d, Path())

    assert list(sorted_dict.keys()) == ["a", "b"]


TEST_DICT = {
    "b": 2,
    "l": [4, 3, 1, 2],
    "a": 1,
    "d": {"x": 1, "y": 2},
    "ld": [{"q": -2, "p": -1}, {"n": 2, "m": 1}],
}
SORTED_DICT = {
    "a": 1,
    "b": 2,
    "d": {"x": 1, "y": 2},
    "l": [1, 2, 3, 4],
    "ld": [{"m": 1, "n": 2}, {"p": -1, "q": -2}],
}


def test_sorted_dict():
    sorted_dict = Sorter.sorted(TEST_DICT)
    assert json.dumps(sorted_dict) == json.dumps(SORTED_DICT)


TEST_LIST = [{"b": 2, "a": 1}, [4, 3, 1, 2]]
SORTED_LIST = [[1, 2, 3, 4], {"a": 1, "b": 2}]


def test_sorted_list():
    sorted_list = Sorter.sorted(TEST_LIST)
    assert json.dumps(sorted_list) == json.dumps(SORTED_LIST)


def test_dict_dict():
    left = {"B": {"b": 2}, "A": {"a": 1}}
    sorted_dict = Sorter.sorted(left)
    assert sorted_dict == {"A": {"a": 1}, "B": {"b": 2}}


def test_list_list():
    left = [[4, 3, 1, 2], []]
    sorted_list = Sorter.sorted(left)
    assert sorted_list == [[], [1, 2, 3, 4]]


NO_SORT = {"sort": [2, 1], "no_sort": [2, 1]}
NO_SORT_RESULT = {"no_sort": [2, 1], "sort": [1, 2]}


def test_no_sort():
    selector = ListLastComponentSelector(component_names=["no_sort"])
    sorter = NoSortListSorter(selectors=selector)
    sorted_dict = Sorter.sorted(NO_SORT, sorters=sorter)
    assert json.dumps(sorted_dict) == json.dumps(NO_SORT_RESULT)


LEFT_FLOAT = [1.1234]


def test_json_encoder_float():
    result = Sorter.sorted(LEFT_FLOAT, normalizers=FloatRoundNormalizer(places=2))
    assert result[0] == 1.12


def test_default_sorter():
    unsorted = {"a": [2, 1], "b": [2, 1]}
    expected = {"a": [1, 2], "b": [1, 2]}
    selector = ListLastComponentSelector(component_names=["a"])
    sorter = DefaultListSorter(selectors=selector)
    sorted_dict = Sorter.sorted(unsorted, sorters=sorter)
    assert json.dumps(sorted_dict) == json.dumps(expected)


class FilteringNoSortListSorter(BaseListSorter):
    def __init__(
        self, *, selectors: SELECTORS = None,
    ):
        """
        Sorter that raises NotSortedError to test BaseListSorter.

        :param selectors: Optional list of selectors to use to select which
            elements this sort runs.
        """
        super().__init__(selectors)

    def _sorted(self, list_: List) -> List:
        """No Op sort."""
        raise NotSortedError


def test_not_sorted():
    unsorted = {"a": [2, 1], "b": [2, 1]}
    expected = {"a": [1, 2], "b": [1, 2]}
    selector = ListLastComponentSelector(component_names=["a"])
    sorter = FilteringNoSortListSorter(selectors=selector)
    sorted_dict = Sorter.sorted(unsorted, sorters=sorter)
    assert json.dumps(sorted_dict) == json.dumps(expected)
