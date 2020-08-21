from pathlib import Path

from ndl_tools import ListLastComponentSelector, BaseListSorter
from ndl_tools import NoSortListSorter


def test_default_no_selector():
    # sorter = DefaultListSorter()
    path = Path("a")
    result = BaseListSorter.sorted([2, 1], path)
    assert result == [1, 2]


def test_no_sort_path_no_selector():
    sorter = NoSortListSorter()
    path = Path("a")
    result = sorter.sorted([2, 1], path, sorters=[sorter])
    assert result == [2, 1]


def test_no_sort_path_match():
    selector = ListLastComponentSelector(["a"])
    sorter = NoSortListSorter(selectors=selector)
    path = Path("a")
    result = sorter.sorted([2, 1], path, sorters=[sorter])
    assert result == [2, 1]


def test_no_sort_path_no_match():
    selector = ListLastComponentSelector(["b"])
    sorter = NoSortListSorter(selectors=selector)
    path = Path("a")
    result = sorter.sorted([2, 1], path, sorters=[sorter])
    assert result == [1, 2]
