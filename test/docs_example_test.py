from ndl_tools import Differ

OBJ_1 = {"a": 1.0, "b": 2.0}
OBJ_2 = {"a": 1.01, "b": 2.01}


def float_mismatch():
    differ = Differ()
    result = differ.diff(OBJ_1, OBJ_2)
    assert not result
    print(result.support)


def test_float_mismatch():
    print()
    float_mismatch()
