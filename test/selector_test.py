from pathlib import Path

from ndl_tools import (
    ListLastComponentSelector,
    ListAnyComponentSelector,
    RegExSelector,
    NegativeSelector,
)

A_TEST_PATH = Path() / "a"
B_TEST_PATH = Path() / "b"
AB_TEST_PATH = Path() / "a" / "b"
BC_TEST_PATH = Path() / "b" / "c"
ABC_TEST_PATH = AB_TEST_PATH / "c"


def test_list_last_selector_base():
    selector = ListLastComponentSelector(["a"])
    assert selector.match(A_TEST_PATH, [selector])
    assert not selector.match(B_TEST_PATH, [selector])


def test_list_list_selector_empty_list():
    selector = ListLastComponentSelector([])
    assert not selector.match(A_TEST_PATH, [selector])


def test_list_any_selector_base():
    selector = ListAnyComponentSelector(["a"])
    assert selector.match(AB_TEST_PATH, [selector])
    assert not selector.match(BC_TEST_PATH, [selector])


def test_list_any_selector_empty_list():
    selector = ListLastComponentSelector([])
    assert not selector.match(AB_TEST_PATH, [selector])


def test_regex():
    selector = RegExSelector("b/c")
    assert selector.match(ABC_TEST_PATH, [selector])
    assert selector.match(BC_TEST_PATH, [selector])
    assert not selector.match(AB_TEST_PATH, [selector])


def test_chained():
    any_selector = ListLastComponentSelector(["c"])
    regex_selector = RegExSelector("a/b")
    assert regex_selector.match(BC_TEST_PATH, [any_selector, regex_selector])


def test_negative():
    selector = ListLastComponentSelector(["a"])
    neg_selector = NegativeSelector(selector=selector)
    assert not neg_selector.match(A_TEST_PATH, [neg_selector])
    assert neg_selector.match(B_TEST_PATH, [neg_selector])
