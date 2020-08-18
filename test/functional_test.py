import datetime
import json
from pathlib import Path

from ndl_tools.normalizer import TodayDateNormalizer
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
    print(json.dumps(data, indent=2))