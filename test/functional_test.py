import json
from pathlib import Path

from ndl_tools import BaseSelector
from ndl_tools import (
    Differ,
    FloatRoundNormalizer,
    StrTodayDateNormalizer,
)


class DateSelector(BaseSelector):
    """
    Match the last component of the path against a list strings.
    """

    def __init__(self):
        """
        Match elements that end with '_date'.
        """
        super().__init__()

    def _match(self, path: Path) -> bool:
        """
        Match the path's last component against the list of match strings.

        :param path:  Path to match.
        :return: True if matched.
        """
        return path.parts[-1].endswith("_date")


def test_diff_example_1():
    data_dpath = Path(__file__).parent
    with (data_dpath / "data" / "1-left-response.json").open("rt") as fp:
        left_dpath = json.loads(fp.read())

    with (data_dpath / "data" / "1-right-response.json").open("rt") as fp:
        right_dpath = json.loads(fp.read())

    differ = Differ()

    # Select all fields that the last element name ends with '_date'
    date_selector = DateSelector()
    # The documents still have their dates as strings.  Run the nomalizer that checks to see
    # if it can parse the string as a date and convert it to today() as a date string.
    date_normalizer = StrTodayDateNormalizer(selectors=date_selector)
    # Normalize floats to have only 3 significant digits.
    float_normalizer = FloatRoundNormalizer(3)

    result = differ.diff(
        left_dpath,
        right_dpath,
        normalizers=[float_normalizer, date_normalizer],
        max_col_width=50,
    )
    assert result
    print(result.support)
