"""
Compare to nested dictionary/list objects.  diff() will return a unix diff like
list of lines of the jsonified object to help locate the differences.
"""
import json
from difflib import HtmlDiff
from json import JSONEncoder
from typing import List, Optional, Type

from .formatter import Formatter
from .list_sorter import LIST_SORTERS
from .normalizer import NORMALIZERS
from .sorter import Sorter, NDLElement


class DiffResult:
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

    @staticmethod
    def diff(
        left: NDLElement,
        right: NDLElement,
        cls: Optional[Type[JSONEncoder]] = None,
        sorters: LIST_SORTERS = None,
        normalizers: NORMALIZERS = None,
        max_col_width: Optional[int] = 20,
    ) -> DiffResult:
        """
        Show the difference of two objects.  Unix like diff results.
        :param left: Test object
        :param right: Expected object
        :param cls: JSON Encoder if any fields aren't JSON encodable.
        :param sorters: Sorters for list elements.
        :param normalizers: Normalizers for leaf elements.
        :param max_col_width: Maximum column width of diff output.
        :return: True if match.
        """
        if normalizers:
            normalizers = (
                normalizers if isinstance(normalizers, list) else [normalizers]
            )
        sorted_left = Sorter.sorted(left, sorters=sorters, normalizers=normalizers)
        sorted_right = Sorter.sorted(right, sorters=sorters, normalizers=normalizers)
        differ = HtmlDiff()

        result = differ.make_file(
            json.dumps(sorted_left, indent=2, cls=cls).split("\n"),
            json.dumps(sorted_right, indent=2, cls=cls).split("\n"),
        )
        match, support = Formatter(max_col_width=max_col_width).format(result)
        return DiffResult(match, support)
