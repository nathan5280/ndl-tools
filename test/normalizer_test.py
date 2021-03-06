import datetime
from pathlib import Path

from ndl_tools import (
    DefaultNormalizer,
    FloatRoundNormalizer,
    TodayDateNormalizer,
    ListLastComponentSelector,
    StrTodayDateNormalizer,
    PathNormalizer,
)


def test_default_normalizer():
    path = Path("a")
    normalizer = DefaultNormalizer()
    result = normalizer.normalize(1.0001, path, normalizers=[normalizer])
    assert result == 1.0001


def test_round_normalizer_no_selector():
    path = Path("a")
    normalizer = FloatRoundNormalizer(2)
    result = normalizer.normalize(1.0001, path, normalizers=[normalizer])
    assert result == 1.00


def test_round_normalizer_match():
    path = Path("a")
    selector = ListLastComponentSelector(["a"])
    normalizer = FloatRoundNormalizer(2, selectors=selector)
    result = normalizer.normalize(1.0001, path, normalizers=[normalizer])
    assert result == 1.00


def test_round_normalizer_no_match():
    path = Path("a")
    selector = ListLastComponentSelector(["b"])
    normalizer = FloatRoundNormalizer(2, selectors=selector)
    result = normalizer.normalize(1.0001, path, normalizers=[normalizer])
    assert result == 1.0001


def test_today_date_normalizer():
    path = Path("a")
    normalizer = TodayDateNormalizer()
    data = datetime.date(1999, 1, 1)
    result = normalizer.normalize(data, path, normalizers=[normalizer])
    assert result == datetime.date.today()


def test_today_date_normalizer_not_normalized():
    path = Path("a")
    normalizer = TodayDateNormalizer()
    data = 1
    result = normalizer.normalize(data, path, normalizers=[normalizer])
    assert result == 1


def test_str_today_date_not_iso():
    path = Path("a")
    normalizer = StrTodayDateNormalizer()
    data = "20-1-1"
    result = normalizer.normalize(data, path, normalizers=[normalizer])
    assert result == "20-1-1"


def test_path():
    path = Path("a")
    normalizer = PathNormalizer(num_components=2)
    data = str(Path("c:/a/b/c"))
    result = normalizer.normalize(data, path, normalizers=[normalizer])
    assert result == "b/c"


def test_path_not_normalized():
    path = Path("a")
    normalizer = PathNormalizer(num_components=2)
    data = 5
    result = normalizer.normalize(data, path, normalizers=[normalizer])
    assert result == data