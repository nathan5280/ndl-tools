from ndl_tools.differ import difference

LEFT1 = {"v1": 1, "d1": {"d1_v1": 1.1, "d1_v2": 1.2}, "l1": [10, 20, 30]}

RIGHT1 = LEFT1


def test_dev():
    difference(LEFT1, RIGHT1)
