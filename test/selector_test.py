from pathlib import Path

from ndl_tools import (
    ListLastComponentSelector,
    ListAnyComponentSelector,
    RegExSelector,
    AllSelector,
    NegativeSelector,
)

A_TEST_PATH = Path() / "a"
B_TEST_PATH = Path() / "b"
AB_TEST_PATH = Path() / "a" / "b"
BC_TEST_PATH = Path() / "b" / "c"
ABC_TEST_PATH = AB_TEST_PATH / "c"


def test_list_last_selector_base():
    selector = ListLastComponentSelector(["a"])
    assert selector.match(A_TEST_PATH)
    assert not selector.match(B_TEST_PATH)


def test_match_all():
    selector = AllSelector()
    assert selector.match(A_TEST_PATH)


def test_list_list_selector_empty_list():
    selector = ListLastComponentSelector([])
    assert not selector.match(A_TEST_PATH)


def test_list_any_selector_base():
    selector = ListAnyComponentSelector(["a"])
    assert selector.match(AB_TEST_PATH)
    assert not selector.match(BC_TEST_PATH)


def test_list_any_selector_empty_list():
    selector = ListLastComponentSelector([])
    assert not selector.match(AB_TEST_PATH)


def test_regex():
    selector = RegExSelector("b/c")
    assert selector.match(ABC_TEST_PATH)
    assert selector.match(BC_TEST_PATH)
    assert not selector.match(AB_TEST_PATH)


def test_chained():
    any_selector = ListLastComponentSelector(["c"])
    regex_selector = RegExSelector("a/b", parent_selector=any_selector)
    assert regex_selector.match(BC_TEST_PATH)


def test_negative():
    selector = ListLastComponentSelector(["a"])
    neg_selector = NegativeSelector(selector=selector)
    assert not neg_selector.match(A_TEST_PATH)
    assert neg_selector.match(B_TEST_PATH)
