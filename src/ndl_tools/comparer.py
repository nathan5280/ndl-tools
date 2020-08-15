"""
Compare to nested dictionary/list objects.  diff() will return a unix diff like
list of lines of the jsonified object to help locate the differences.
"""
import json
from difflib import Differ, HtmlDiff
from json import JSONEncoder
from typing import Union, Any, Iterable, Mapping, List, Optional, Type

from ndl_tools.sorter import Sorter, NDLElement


class CompareResult:
    """
    Result of a compare or diff.   Acts like a bool for testing purposes.
    Provides supporting information for the match.
    """

    def __init__(self, match: bool, support: List[str]):
        self._match = match
        self.support = support

    def __bool__(self) -> bool:
        return self._match


class Comparer:
    """
    Provides comparision and difference methods for two objects of
    nested dictionary/lists.   The process is to first sort the two objects
    and then compare them or jsonify them and compare the individual lines.
    """

    @staticmethod
    def compare(test: NDLElement, expected: NDLElement) -> CompareResult:
        """
        Compare to nested dictionary/list objects.
        :param test: Test object
        :param expected: Expected object
        :return: True if match.
        """
        sorted_test = Sorter.sorted(test)
        sorted_expected = Sorter.sorted(expected)
        return CompareResult(sorted_test == sorted_expected, [])

    @staticmethod
    def diff(
        test: NDLElement, expected: NDLElement, cls: Optional[Type[JSONEncoder]] = None
    ) -> CompareResult:
        """
        Show the difference of two objects.  Unix like diff results.
        :param test: Test object
        :param expected: Expected object
        :param cls: JSON Encoder if any fields aren't JSON encodable.
        :return: True if match.
        """
        sorted_test = Sorter.sorted(test)
        sorted_expected = Sorter.sorted(expected)
        differ = Differ()
        result = differ.compare(
            json.dumps(sorted_test, indent=2, cls=cls).split("\n"),
            json.dumps(sorted_expected, indent=2, cls=cls).split("\n"),
        )
        lines = list(result)
        match = not any([line[0] in ["-", "+", "?"] for line in lines])
        return CompareResult(match, lines)

    @staticmethod
    def html_diff(
        test: NDLElement, expected: NDLElement, cls: Optional[Type[JSONEncoder]] = None
    ) -> str:
        """
        Show the difference of two objects.  Unix like diff results.
        :param test: Test object
        :param expected: Expected object
        :param cls: JSON Encoder if any fields aren't JSON encodable.
        :return: True if match.
        """
        sorted_test = Sorter.sorted(test)
        sorted_expected = Sorter.sorted(expected)
        differ = HtmlDiff()
        result = differ.make_file(
            json.dumps(sorted_test, indent=2, cls=cls).split("\n"),
            json.dumps(sorted_expected, indent=2, cls=cls).split("\n"),
        )
        return result
