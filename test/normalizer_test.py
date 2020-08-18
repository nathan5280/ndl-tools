import datetime
from pathlib import Path

from ndl_tools.normalizer import DefaultNormalizer, FloatRoundNormalizer, TodayDateNormalizer
from ndl_tools.path_matcher import ListLastComponentPathMatcher


def test_default_normalizer():
    path = Path("a")
    normalizer = DefaultNormalizer()
    result = normalizer.normalize(1.0001, path)
    assert result == 1.0001


def test_round_normalizer_no_matcher():
    path = Path("a")
    normalizer = FloatRoundNormalizer(2)
    result = normalizer.normalize(1.0001, path)
    assert result == 1.00


def test_round_normalizer_match():
    path = Path("a")
    matcher = ListLastComponentPathMatcher(["a"])
    normalizer = FloatRoundNormalizer(2, path_matcher=matcher)
    result = normalizer.normalize(1.0001, path)
    assert result == 1.00


def test_round_normalizer_no_match():
    path = Path("a")
    matcher = ListLastComponentPathMatcher(["b"])
    normalizer = FloatRoundNormalizer(2, path_matcher=matcher)
    result = normalizer.normalize(1.0001, path)
    assert result == 1.0001


def test_today_date_normalizer():
    path = Path("a")
    normalizer = TodayDateNormalizer()
    data = datetime.date(1999, 1, 1)
    result = normalizer.normalize(data, path)
    assert result == datetime.date.today()
