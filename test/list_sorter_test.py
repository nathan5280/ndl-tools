import json
from pathlib import Path

from ndl_tools.list_sorter import DefaultListSorter, NoSortListSorter
from ndl_tools.path_matcher import ListLastComponentPathMatcher


def test_default_no_path_matcher():
    sorter = DefaultListSorter()
    path = Path("a")
    result = sorter.sorted([2, 1], path)
    assert result == [1, 2]


def test_default_path_match():
    matcher = ListLastComponentPathMatcher(["a"])
    sorter = DefaultListSorter(path_matcher=matcher)
    path = Path("a")
    result = sorter.sorted([2, 1], path)
    assert result == [1, 2]


def test_default_no_path_match():
    matcher = ListLastComponentPathMatcher(["b"])
    sorter = DefaultListSorter(path_matcher=matcher)
    path = Path("a")
    result = sorter.sorted([2, 1], path)
    assert result == [1, 2]


def test_no_sort_path_no_path_matcher():
    sorter = NoSortListSorter()
    path = Path("a")
    result = sorter.sorted([2, 1], path)
    assert result == [2, 1]


def test_no_sort_path_match():
    matcher = ListLastComponentPathMatcher(["a"])
    sorter = NoSortListSorter(path_matcher=matcher)
    path = Path("a")
    result = sorter.sorted([2, 1], path)
    assert result == [2, 1]


def test_no_sort_path_no_match():
    matcher = ListLastComponentPathMatcher(["b"])
    sorter = NoSortListSorter(path_matcher=matcher)
    path = Path("a")
    result = sorter.sorted([2, 1], path)
    assert result == [1, 2]
