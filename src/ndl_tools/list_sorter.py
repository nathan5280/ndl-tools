"""
ListSorters used to control if and how Lists are sorted.  Really there are only two
choices.  Sort or don't sort.  The sorter can be applied to the List elements by
the Selector that is associated with the sorter.
"""
from abc import abstractmethod
from pathlib import Path
from typing import List, Optional

from .selector import BaseSelector, AllSelector


class BaseListSorter:
    """
    Base list sorter implements the chaining logic.
    """
    def __init__(
        self,
        parent_sorter: Optional["BaseListSorter"] = None,
        selector: Optional[BaseSelector] = None,
    ):
        """
        Initialize the sorter with optional parent sorter and selector.

        :param parent_sorter: Optional sorter to run if this sorted isn't selected
            by the selector.
        :param selector: Optional selector to use to select which
            elements this sort runs.
        """
        self._parent_sorter = parent_sorter
        self._selector = selector or AllSelector()

    def sorted(self, list_: List, path: Path) -> List:
        """
        Run all the sorters until one applied to sort or not sort the list.

        :param list_: List to sort.
        :param path: Path to the element.
        :return: Sorted list.
        """
        if self._selector.match(path):
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
        selector: Optional[BaseSelector] = None,
    ):
        """
        Standard Python sorted() sorter.

        :param parent_sorter: Optional sorter to run if this sorted isn't selected
            by the selector.
        :param selector: Optional selector to use to select which
            elements this sort runs.
        """
        super().__init__(parent_sorter, selector)

    def _sorted(self, list_: List) -> List:
        """Default Python sorted()."""
        return sorted(list_)


class NoSortListSorter(BaseListSorter):
    def __init__(
        self,
        *,
        parent_sorter: Optional[BaseListSorter] = None,
        selector: Optional[BaseSelector] = None,
    ):
        """
        No Op sorter.

        :param parent_sorter: Optional sorter to run if this sorted isn't selected
            by the selector.
        :param selector: Optional selector to use to select which
            elements this sort runs.
        """
        super().__init__(parent_sorter, selector)

    def _sorted(self, list_: List) -> List:
        """No Op sort."""
        return list_
