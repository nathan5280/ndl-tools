import json
from pathlib import Path

from ndl_tools.iterable_sorter import DefaultIterableSorter, NoSortIterableSorter
from ndl_tools.path_matcher import ListLastComponentPathMatcher


def test_default_no_path_matcher():
    sorter = DefaultIterableSorter()
    path = Path("a")
    result = sorter.sorted([2, 1], path)
    assert result == [1, 2]


def test_default_path_match():
    matcher = ListLastComponentPathMatcher(["a"])
    sorter = DefaultIterableSorter(path_matcher=matcher)
    path = Path("a")
    result = sorter.sorted([2, 1], path)
    assert result == [1, 2]


def test_default_no_path_match():
    matcher = ListLastComponentPathMatcher(["b"])
    sorter = DefaultIterableSorter(path_matcher=matcher)
    path = Path("a")
    result = sorter.sorted([2, 1], path)
    assert result == [1, 2]


def test_no_sort_path_no_path_matcher():
    sorter = NoSortIterableSorter()
    path = Path("a")
    result = sorter.sorted([2, 1], path)
    assert result == [2, 1]


def test_no_sort_path_match():
    matcher = ListLastComponentPathMatcher(["a"])
    sorter = NoSortIterableSorter(path_matcher=matcher)
    path = Path("a")
    result = sorter.sorted([2, 1], path)
    assert result == [2, 1]


def test_no_sort_path_no_match():
    matcher = ListLastComponentPathMatcher(["b"])
    sorter = NoSortIterableSorter(path_matcher=matcher)
    path = Path("a")
    result = sorter.sorted([2, 1], path)
    assert result == [1, 2]
