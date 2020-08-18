"""
Compare to nested dictionary/list objects.  diff() will return a unix diff like
list of lines of the jsonified object to help locate the differences.
"""
import json
from difflib import Differ as _Differ, HtmlDiff
from json import JSONEncoder
from pathlib import Path
from typing import List, Optional, Type

from ndl_tools.formatter import Formatter
from ndl_tools.sorter import Sorter, NDLElement, BaseIterableSorter, BaseNormalizer


class DifferResult:
    """
    Result of a compare or diff.   Acts like a bool for testing purposes.
    Provides supporting information for the match.
    """

    def __init__(self, match: bool, support: List[str]):
        self._match = match
        self.support = support

    def __bool__(self) -> bool:
        return self._match


class Differ:
    """
    Provides comparision and difference methods for two objects of
    nested dictionary/lists.   The process is to first sort the two objects
    and then compare them or jsonify them and compare the individual lines.
    """

    # @staticmethod
    # def diff(
    #     left: NDLElement,
    #     right: NDLElement,
    #     cls: Optional[JSONEncoder] = None,
    #     sorter: Optional[BaseIterableSorter] = None,
    #     normalizer: Optional[BaseNormalizer] = None,
    # ) -> DifferResult:
    #     """
    #     Show the difference of two objects.  Unix like diff results.
    #     :param left: Test object
    #     :param right: Expected object
    #     :param cls: JSON Encoder if any fields aren't JSON encodable.
    #     :param sorter: Sorter for iterable elements.
    #     :param normalizer: Normalizer for leaf elements.
    #     :return: True if match.
    #     """
    #     l_sorted = Sorter.sorted(left, sorter=sorter, normalizer=normalizer)
    #     r_sorted = Sorter.sorted(right, sorter=sorter, normalizer=normalizer)
    #     differ = _Differ()
    #     l_json = json.dumps(l_sorted, indent=2, cls=cls)
    #     r_json = json.dumps(r_sorted, indent=2, cls=cls)
    #     result = differ.compare(l_json.split("\n"), r_json.split("\n"),)
    #     lines = list(result)
    #     match = not any([line[0] in ["-", "+", "?"] for line in lines])
    #     return DifferResult(match, lines)

    @staticmethod
    def diff(
        left: NDLElement,
        right: NDLElement,
        cls: Optional[Type[JSONEncoder]] = None,
        sorter: Optional[BaseIterableSorter] = None,
        normalizer: Optional[BaseNormalizer] = None,
    ) -> DifferResult:
        """
        Show the difference of two objects.  Unix like diff results.
        :param left: Test object
        :param right: Expected object
        :param cls: JSON Encoder if any fields aren't JSON encodable.
        :param sorter: Sorter for iterable elements.
        :param normalizer: Normalizer for leaf elements.
        :return: True if match.
        """
        sorted_left = Sorter.sorted(left, sorter=sorter, normalizer=normalizer)
        sorted_right = Sorter.sorted(right, sorter=sorter, normalizer=normalizer)
        differ = HtmlDiff()

        result = differ.make_file(
            json.dumps(sorted_left, indent=2, cls=cls).split("\n"),
            json.dumps(sorted_right, indent=2, cls=cls).split("\n"),
        )
        match, support = Formatter().format(result)
        return DifferResult(match, support)
