"""
ListSorters used to control if and how Lists are sorted.  Really there are only two
choices.  Sort or don't sort.  The sorter can be applied to the List elements by
the PathMatcher that is associated with the sorter.
"""
from abc import abstractmethod
from pathlib import Path
from typing import List, Optional

from ndl_tools.path_matcher import BasePathMatcher, AllPathMatcher


class BaseListSorter:
    """
    Base list sorter implements the chaining logic.
    """
    def __init__(
        self,
        parent_sorter: Optional["BaseListSorter"] = None,
        path_matcher: Optional[BasePathMatcher] = None,
    ):
        """
        Initialize the sorter with optional parent sorter and path matcher.

        :param parent_sorter: Optional sorter to run if this sorted isn't selected
            by the path matcher.
        :param path_matcher: Optional path matcher to use to select which
            elements this sort runs.
        """
        self._parent_sorter = parent_sorter
        self._path_matcher = path_matcher or AllPathMatcher()

    def sorted(self, list_: List, path: Path) -> List:
        """
        Run all the sorters until one applied to sort or not sort the list.

        :param list_: List to sort.
        :param path: Path to the element.
        :return: Sorted list.
        """
        if self._path_matcher.match(path):
            return self._sorted(list_)
        return self._parent_sorter.sorted(path) if self._parent_sorter else sorted(list_)

    @abstractmethod
    def _sorted(self, list_: List) -> List:
        """
        Prototype for the core sorting logic implemented in the subclass.

        :param list_: List to sort.
        :return: Sorted list.
        """
        pass


class DefaultListSorter(BaseListSorter):
    def __init__(
        self,
        *,
        parent_sorter: Optional[BaseListSorter] = None,
        path_matcher: Optional[BasePathMatcher] = None,
    ):
        """
        Standard Python sorted() sorter.

        :param parent_sorter: Optional sorter to run if this sorted isn't selected
            by the path matcher.
        :param path_matcher: Optional path matcher to use to select which
            elements this sort runs.
        """
        super().__init__(parent_sorter, path_matcher)

    def _sorted(self, list_: List) -> List:
        """Default Python sorted()."""
        return sorted(list_)


class NoSortListSorter(BaseListSorter):
    def __init__(
        self,
        *,
        parent_sorter: Optional[BaseListSorter] = None,
        path_matcher: Optional[BasePathMatcher] = None,
    ):
        """
        No Op sorter.

        :param parent_sorter: Optional sorter to run if this sorted isn't selected
            by the path matcher.
        :param path_matcher: Optional path matcher to use to select which
            elements this sort runs.
        """
        super().__init__(parent_sorter, path_matcher)

    def _sorted(self, list_: List) -> List:
        """No Op sort."""
        return list_
