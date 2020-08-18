"""
IterableSorters used to control if and how Iterables are sorted.  Really there are only two
choices.  Sort or don't sort.  The sorter can be applied to the Iterable elements by
the PathMatcher that is associated with the sorter.
"""
from abc import abstractmethod
from pathlib import Path
from typing import Iterable, Optional

from ndl_tools.path_matcher import BasePathMatcher, AllPathMatcher


class BaseIterableSorter:
    """
    Base iterable sorter implements the chaining logic.
    """
    def __init__(
        self,
        parent_sorter: Optional["BaseIterableSorter"] = None,
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

    def sorted(self, iterable: Iterable, path: Path) -> Iterable:
        """
        Run all the sorters until one applied to sort or not sort the list.

        :param iterable: Iterable to sort.
        :param path: Path to the element.
        :return: Sorted iterable.
        """
        if self._path_matcher.match(path):
            return self._sorted(iterable)
        return self._parent_sorter.sorted(path) if self._parent_sorter else sorted(iterable)

    @abstractmethod
    def _sorted(self, iterable: Iterable) -> Iterable:
        """
        Prototype for the core sorting logic implemented in the subclass.

        :param iterable: Iterable to sort.
        :return: Sorted iterable.
        """
        pass


class DefaultIterableSorter(BaseIterableSorter):
    def __init__(
        self,
        *,
        parent_sorter: Optional[BaseIterableSorter] = None,
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

    def _sorted(self, iterable: Iterable) -> Iterable:
        """Default Python sorted()."""
        return sorted(iterable)


class NoSortIterableSorter(BaseIterableSorter):
    def __init__(
        self,
        *,
        parent_sorter: Optional[BaseIterableSorter] = None,
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

    def _sorted(self, iterable: Iterable) -> Iterable:
        """No Op sort."""
        return iterable
