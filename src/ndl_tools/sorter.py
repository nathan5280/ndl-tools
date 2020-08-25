"""
Sort nested dictionary/lists.  The sort order isn't really important,
just that it is consistent.

Alternative ListSorters can be applied to elements selected by the
by Selectors.
"""
from pathlib import Path
from typing import Any, Union, Mapping, Optional, List, Dict

from .list_sorter import BaseListSorter, LIST_SORTERS
from .normalizer import BaseNormalizer, NORMALIZERS

NDLElement = Union[Mapping, List, Any]


class SortedMapping(dict):
    """
    Replacement for a dictionary that sorts it's keys when it is created.
    Does depth first replacement of dicts and lists so that when it sorts
    it is using the sorted version of its contents.
    """

    def __init__(
        self,
        data: Mapping,
        path: Path,
        sorters: Optional[List[BaseListSorter]] = None,
        normalizers: Optional[List[BaseNormalizer]] = None,
    ):
        """
        Construct a new dict that is sorted.
        :param data: Unsorted dictionary.
        :param path: Path to current element.
        :param sorters: Sorters for list elements.
        :param normalizers: Normalizers for leaf nodes.
        """
        super().__init__(
            **{
                k: Sorter._sorted(data[k], path / k, sorters, normalizers)
                for k in sorted(data.keys())
            }
        )

    def __lt__(self, other) -> bool:
        """
        Compare two objects.  If they are both SortedMapping then compare them
        as dictionaries.  Otherwise, just compare their class types.  Order isn't
        really important.  It just needs to be consistent.
        :param other: Object to compare.
        :return: bool
        """
        if isinstance(other, SortedMapping):
            return list(self.items()) < list(other.items())
        else:
            # The order doesn't really matter here as long as it is consistent.
            return str(self.__class__) < str(other.__class__)


class SortedList(list):
    """
    Replacement for a list that sorts it's keys when it is created.
    Does depth first replacement of dicts and lists so that when it sorts
    it is using the sorted version of its contents.
    """

    def __init__(
        self,
        list_: List,
        path: Path,
        sorters: Optional[List[BaseListSorter]] = None,
        normalizers: Optional[List[BaseNormalizer]] = None,
    ):
        """
        Construct a new list that is sorted.
        :param list_: Unsorted list.
        :param path: Path to the current element.
        :param sorters: Sorters for list elements.
        :param normalizers: Normalizers for leaf elements.
        """
        sorted_children = [
            Sorter._sorted(v, path / f"[{i}]", sorters, normalizers)
            for i, v in enumerate(list_)
        ]
        super().__init__(BaseListSorter.sorted(sorted_children, path, sorters))

    def __lt__(self, other) -> bool:
        """
        Compare two objects.  If they are both SortedList then compare them
        as lists.  Otherwise, just compare their class types.  Order isn't
        really important.  It just needs to be consistent.
        :param other: Object to compare.
        :return: bool
        """
        if isinstance(other, SortedList):
            return list(self) < list(other)
        else:
            # The order doesn't really matter here as long as it is consistent.
            return str(self.__class__) < str(other.__class__)


class Sorter:
    @staticmethod
    def _sorted(
        data: NDLElement,
        path: Path,
        sorters: Optional[List[BaseListSorter]] = None,
        normalizers: Optional[List[BaseNormalizer]] = None,
    ) -> Union[SortedMapping, SortedList, Any]:
        """
        Sort a nested dictionary/list.  Used internally to keep the path argument from being exposed in the
        public interface.
        :param data: Object to sort.
        :param path: Path to the current element.
        :param sorter: Sorter for list elements.
        :param normalizers: List of normalizer for leaf elements.
        :return: Sorted object.
        """
        if isinstance(data, Dict):
            return SortedMapping(data, path, sorters, normalizers)
        elif isinstance(data, List):
            return SortedList(data, path, sorters, normalizers)
        else:
            return BaseNormalizer.normalize(data, path, normalizers)

    @staticmethod
    def sorted(
        data: NDLElement,
        *,
        sorters: LIST_SORTERS = None,
        normalizers: NORMALIZERS = None,
    ) -> Union[SortedMapping, SortedList, Any]:
        """
        Sort a nested dictionary/list.
        :param data: Object to sort.
        :param sorters: Sorter for list elements.
        :param normalizers: Normalizer for leaf elements.
        :return: Sorted object.
        """
        if sorters:
            sorters = sorters if isinstance(sorters, list) else [sorters]
        if normalizers:
            normalizers = (
                normalizers if isinstance(normalizers, list) else [normalizers]
            )

        return Sorter._sorted(data, Path(), sorters=sorters, normalizers=normalizers)
