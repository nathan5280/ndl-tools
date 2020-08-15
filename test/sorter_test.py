import json

from ndl_tools.sorter import SortedIterable, SortedMapping, Sorter


def test_sorted_iterable():
    d = [4, 3, 1, 2]
    s = SortedIterable(d)
    assert s == [1, 2, 3, 4]


def test_sorted_mapping():
    d = {"b": 2, "a": 1}
    sorted_dict = SortedMapping(d)

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
    l = {"B": {"b": 2}, "A": {"a": 1}}
    sorted_dict = Sorter.sorted(l)
    assert sorted_dict == {"A": {"a": 1}, "B": {"b": 2}}


def test_list_list():
    l = [[4, 3, 1, 2], []]
    sorted_list = Sorter.sorted(l)
    assert sorted_list == [[], [1, 2, 3, 4]]
