from pathlib import Path

from ndl_tools.list_sorter import DefaultListSorter, NoSortListSorter
from ndl_tools.selector import ListLastComponentSelector


def test_default_no_selector():
    sorter = DefaultListSorter()
    path = Path("a")
    result = sorter.sorted([2, 1], path)
    assert result == [1, 2]


def test_default_path_match():
    selector = ListLastComponentSelector(["a"])
    sorter = DefaultListSorter(selector=selector)
    path = Path("a")
    result = sorter.sorted([2, 1], path)
    assert result == [1, 2]


def test_default_no_path_match():
    selector = ListLastComponentSelector(["b"])
    sorter = DefaultListSorter(selector=selector)
    path = Path("a")
    result = sorter.sorted([2, 1], path)
    assert result == [1, 2]


def test_no_sort_path_no_selector():
    sorter = NoSortListSorter()
    path = Path("a")
    result = sorter.sorted([2, 1], path)
    assert result == [2, 1]


def test_no_sort_path_match():
    selector = ListLastComponentSelector(["a"])
    sorter = NoSortListSorter(selector=selector)
    path = Path("a")
    result = sorter.sorted([2, 1], path)
    assert result == [2, 1]


def test_no_sort_path_no_match():
    selector = ListLastComponentSelector(["b"])
    sorter = NoSortListSorter(selector=selector)
    path = Path("a")
    result = sorter.sorted([2, 1], path)
    assert result == [1, 2]
