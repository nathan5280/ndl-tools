import copy
import datetime
from json import JSONEncoder

from ndl_tools import Differ

TEST_DICT = {"b": 2, "l": [4, 3, 1, 2], "a": 1, "d": {"x": 1, "y": 2}, "ld": [{"n": 2, "m": 1}]}
SORTED_DICT = {"a": 1, "b": 2, "d": {"x": 1, "y": 2}, "l": [1, 2, 3, 4], "ld": [{"m": 1, "n": 2}]}


TEST_LIST = [{"b": 2, "a": 1}, [4, 3, 1, 2]]
SORTED_LIST = [[1, 2, 3, 4], {"a": 1, "b": 2}]


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


def test_html_diff_dict_fail():
    td = copy.deepcopy(TEST_DICT)
    td["l"] = []
    result = Differ.diff(td, SORTED_DICT)
    assert not result
    print(result.support)

