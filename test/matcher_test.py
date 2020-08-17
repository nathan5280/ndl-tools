import re
from pathlib import Path

from ndl_tools.path_matcher import (
    ListLastComponentPathMatcher,
    ListAnyComponentPathMatcher,
    RegExPathMatcher,
    AllPathMatcher,
    NegativePathMatcher)

A_TEST_PATH = Path() / "a"
B_TEST_PATH = Path() / "b"
AB_TEST_PATH = Path() / "a" / "b"
BC_TEST_PATH = Path() / "b" / "c"
ABC_TEST_PATH = AB_TEST_PATH / "c"


def test_list_last_matcher_base():
    matcher = ListLastComponentPathMatcher(["a"])
    assert matcher.match(A_TEST_PATH)
    assert not matcher.match(B_TEST_PATH)


def test_match_all():
    matcher = AllPathMatcher()
    assert matcher.match(A_TEST_PATH)


def test_list_list_matcher_empty_list():
    matcher = ListLastComponentPathMatcher([])
    assert not matcher.match(A_TEST_PATH)


def test_list_any_matcher_base():
    matcher = ListAnyComponentPathMatcher(["a"])
    assert matcher.match(AB_TEST_PATH)
    assert not matcher.match(BC_TEST_PATH)


def test_list_any_matcher_empty_list():
    matcher = ListLastComponentPathMatcher([])
    assert not matcher.match(AB_TEST_PATH)


def test_regex():
    matcher = RegExPathMatcher("b/c")
    assert matcher.match(ABC_TEST_PATH)
    assert matcher.match(BC_TEST_PATH)
    assert not matcher.match(AB_TEST_PATH)


def test_chained():
    any_matcher = ListLastComponentPathMatcher(["c"])
    regex_matcher = RegExPathMatcher("a/b", parent_matcher=any_matcher)
    assert regex_matcher.match(BC_TEST_PATH)


def test_negative():
    matcher = ListLastComponentPathMatcher(["a"])
    neg_matcher = NegativePathMatcher(matcher)
    assert not neg_matcher.match(A_TEST_PATH)
    assert neg_matcher.match(B_TEST_PATH)
