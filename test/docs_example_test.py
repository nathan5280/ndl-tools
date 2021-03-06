from ndl_tools import Differ, FloatRoundNormalizer, ListLastComponentSelector

OBJ_1 = {"a": 1.0, "b": 2.01}
OBJ_2 = {"a": 1.01, "b": 2.011}


def float_mismatch():
    differ = Differ()
    result = differ.diff(OBJ_1, OBJ_2)
    assert not result
    print(result.support)


def test_float_mismatch():
    print()
    float_mismatch()


def float_match():
    differ = Differ()
    float_round_normalizer = FloatRoundNormalizer(places=1)
    result = differ.diff(OBJ_1, OBJ_2, normalizers=[float_round_normalizer])
    assert result
    print(result.support)


def test_float_normalized():
    print()
    float_match()


def float_two_precision_match():
    differ = Differ()
    # Normalize the 'a' element to 1 decimal place.
    a_selector = ListLastComponentSelector(component_names=["a"])
    one_float_round_normalizer = FloatRoundNormalizer(places=1, selectors=[a_selector])

    # Normalize the 'b' element to 2 decimal places.
    b_selector = ListLastComponentSelector(component_names=["b"])
    two_float_round_normalizer = FloatRoundNormalizer(places=2, selectors=[b_selector])

    result = differ.diff(
        OBJ_1,
        OBJ_2,
        normalizers=[two_float_round_normalizer, one_float_round_normalizer],
    )
    assert result
    print(result.support)


def test_float_two_precision_match():
    print()
    float_two_precision_match()


def selector_multiple_match():
    differ = Differ()

    a_selector = ListLastComponentSelector(component_names=["a"])
    b_selector = ListLastComponentSelector(component_names=["b"])
    float_round_normalizer = FloatRoundNormalizer(
        places=1, selectors=[a_selector, b_selector]
    )

    result = differ.diff(OBJ_1, OBJ_2, normalizers=[float_round_normalizer])
    assert result
    print(result.support)


def test_selector_multiple_match():
    print()
    selector_multiple_match()
