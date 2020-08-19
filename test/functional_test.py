import datetime
import json
from pathlib import Path
from typing import Optional, Any, List

from ndl_tools.differ import Differ
from ndl_tools.normalizer import TodayDateNormalizer, BaseNormalizer, FloatRoundNormalizer
from ndl_tools.selector import BaseSelector
from ndl_tools.sorter import Sorter


def test_1_data():
    left_1_data = {"date": datetime.date(1999, 1, 1), "float": 1.0}
    right_1_data = {"date": datetime.date(1999, 2, 2), "float": 1.001}

    date_normalizer = TodayDateNormalizer


def test_sort_johns():
    sorter = Sorter()
    with Path(".data/deductible_plan_response.json").open("rt") as fp:
        data = json.loads(fp.read())
    data = sorter.sorted(data)
    with Path(".data/deductible_plan_response_sorted.json").open("wt") as fp:
        fp.write(json.dumps(data, indent=2))

    with Path(".data/given_deductible_plan_response.json").open("rt") as fp:
        data = json.loads(fp.read())
    data = sorter.sorted(data)
    with Path(".data/given_deductible_plan_response_sorted.json").open("wt") as fp:
        fp.write(json.dumps(data, indent=2))


class StrTodayDateNormalizer(BaseNormalizer):
    def __init__(
        self,
        *,
        parent_normalizer: Optional["BaseNormalizer"] = None,
        selector: Optional[BaseSelector] = None,
    ):
        """
        Overwrite string representation of a date to today().

        :param parent_normalizer: Optional parent normalizer to run if this normalizer
            isn't selected by the selector.
        :param selector: Optional selector to use to select which
            elements this normalizer runs.
        """
        super().__init__(parent_normalizer, selector)

    def _normalize(self, element: Any) -> Any:
        if isinstance(element, str):
            return datetime.date.today().isoformat()
        return element


class DateSelector(BaseSelector):
    """
    Match the last component of the path against a list strings.
    """

    def __init__(self, *, selector: Optional[BaseSelector] = None):
        """
        Match elements that end with '_date'.

        :param selector: Optional parent selector.
        """
        super().__init__(selector)

    def _match(self, path: Path) -> bool:
        """
        Match the path's last component against the list of match strings.

        :param path:  Path to match.
        :return: True if matched.
        """
        return path.parts[-1].endswith("_date")


def test_diff_johns2():
    sorter = Sorter()
    with Path(".data/deductible_plan_response.json").open("rt") as fp:
        data = json.loads(fp.read())

    with Path(".data/deductible_plan_response2.json").open("rt") as fp:
        data2 = json.loads(fp.read())

    differ = Differ()

    date_selector = DateSelector()
    date_normalizer = StrTodayDateNormalizer(selector=date_selector)
    float_normalizer = FloatRoundNormalizer(4, parent_normalizer=date_normalizer)

    result = differ.diff(data, data2, normalizer=float_normalizer, max_col_width=50)
    print(result.support)
