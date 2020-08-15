import copy
import datetime
from json import JSONEncoder
from pathlib import Path

from ndl_tools.differ import Differ

TEST_DICT = {"b": 2, "l": [4, 3, 1, 2], "a": 1, "d": {"x": 1, "y": 2}, "ld": [{"n": 2, "m": 1}]}
SORTED_DICT = {"a": 1, "b": 2, "d": {"x": 1, "y": 2}, "l": [1, 2, 3, 4], "ld": [{"m": 1, "n": 2}]}


def test_compare_dict():
    match = Differ.compare(TEST_DICT, SORTED_DICT)
    assert match


TEST_LIST = [{"b": 2, "a": 1}, [4, 3, 1, 2]]
SORTED_LIST = [[1, 2, 3, 4], {"a": 1, "b": 2}]


def test_compare_list():
    match = Differ.compare(TEST_LIST, SORTED_LIST)
    assert match


def test_compare_dict_fail():
    td = copy.deepcopy(TEST_DICT)
    td["l"] = []
    match = Differ.compare(td, SORTED_DICT)
    assert not match


def test_compare_list_fail():
    tl = copy.deepcopy(TEST_LIST)
    tl[0] = []
    match = Differ.compare(tl, SORTED_LIST)
    assert not match


def test_diff_dict():
    match = Differ.diff(TEST_DICT, SORTED_DICT)
    assert match


def test_diff_dict_fail():
    td = copy.deepcopy(TEST_DICT)
    td["l"] = []
    match = Differ.diff(td, SORTED_DICT)
    assert not match


def test_diff_list():
    result = Differ.diff(TEST_LIST, SORTED_LIST)
    assert result


def test_diff_list_fail():
    tl = copy.deepcopy(TEST_LIST)
    tl[0] = []
    result = Differ.diff(tl, SORTED_LIST)
    for l in result.support:
        print(l)
    assert not result


class DateJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        return JSONEncoder.default(obj)


def test_json_encoder():
    d1 = {"date": datetime.date.today()}
    result = Differ.diff(d1, d1, cls=DateJSONEncoder)
    assert result


def test_nested_dict_equal():
    d1 = {"a": 1, "b": {"x": 1, "y": 2}}
    d2 = {"a": 1, "b": {"x": 2, "y": 2}}
    result = Differ.compare(d1, d2)
    assert not result

    result = Differ.diff(d1, d2)
    assert not result


def test_nested_list_equal():
    d1 = [1, 2, [1, 2]]
    d2 = [1, 2, [2, 2]]
    result = Differ.compare(d1, d2)
    assert not result

    result = Differ.diff(d1, d2)
    assert not result


def test_html_diff_dict_fail():
    td = copy.deepcopy(TEST_DICT)
    td["l"] = []
    result = Differ.html_diff(td, SORTED_DICT)
    with Path(".data/diff.html").open("wt") as fp:
        fp.write(result)

