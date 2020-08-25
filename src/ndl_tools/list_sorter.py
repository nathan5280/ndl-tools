"""
ListSorters used to control if and how Lists are sorted.  Really there are only two
choices.  Sort or don't sort.  The sorter can be applied to the List elements by
the Selector that is associated with the sorter.
"""
from abc import abstractmethod
from pathlib import Path
from typing import List, Optional, Union

from .selector import BaseSelector, SELECTORS


class NotSortedError(Exception):
    """The sorter was not applied to the list."""


class BaseListSorter:
    """
    Base list sorter implements the chaining logic.
    """

    def __init__(
        self, selectors: SELECTORS = None,
    ):
        """
        Initialize the sorter with optional parent sorter and selector.

        :param selectors: Optional selectors to use to select which
            elements this sort runs.
        """
        if selectors:
            self._selectors = selectors if isinstance(selectors, list) else [selectors]
        else:
            # No selectors specified
            self._selectors = None

    @staticmethod
    def sorted(
        list_: List, path: Path, sorters: Optional[List["BaseListSorter"]] = None
    ) -> List:
        """
        Run all the sorters until one applied to sort or not sort the list.

        :param list_: List to sort.
        :param path: Path to the element.
        :param sorters: List of sorters to use to sort the lists.
        :return: Sorted list.
        """
        if not sorters:
            return sorted(list_)

        for sorter in sorters:
            if BaseSelector.match(path, sorter._selectors):
                try:
                    return sorter._sorted(list_)
                except NotSortedError:
                    continue
        return sorted(list_)

    @abstractmethod
    def _sorted(self, list_: List) -> List:
        """
        Prototype for the core sorting logic implemented in the subclass.

        :param list_: List to sort.
        :return: Sorted list.
        """
        pass  # pragma: no cover


LIST_SORTERS = Optional[Union[BaseListSorter, List[BaseListSorter]]]


class DefaultListSorter(BaseListSorter):
    def __init__(
        self, *, selectors: SELECTORS = None,
    ):
        """
        Standard Python sorted() sorter.

        :param selectors: Optional list of selectors to use to select which
            elements this sort runs.
        """
        super().__init__(selectors)

    def _sorted(self, list_: List) -> List:
        """Default Python sorted()."""
        return sorted(list_)


class NoSortListSorter(BaseListSorter):
    def __init__(
        self, *, selectors: SELECTORS = None,
    ):
        """
        No Op sorter.

        :param selectors: Optional list of selectors to use to select which
            elements this sort runs.
        """
        super().__init__(selectors)

    def _sorted(self, list_: List) -> List:
        """No Op sort."""
        return list_
