"""
Sort nested dictionary/lists.  The sort order isn't really important,
just that it is consistent.
"""
from abc import abstractmethod
from pathlib import Path
from typing import Any, Union, Mapping, Iterable, Optional

NDLElement = Union[Mapping, Iterable, Any]


class IterableSorter:
    @abstractmethod
    def sorted(self, iterable: Iterable, path: Path) -> Iterable:
        pass


class DefaultIterableSorter(IterableSorter):
    def sorted(self, iterable: Iterable, path: Path) -> Iterable:
        return sorted(iterable)


class SortedMapping(dict):
    """
    Replacement for a dictionary that sorts it's keys when it is created.
    Does depth first replacement of dicts and lists so that when it sorts
    it is using the sorted version of its contents.
    """

    def __init__(self, data: Mapping, path: Path, sorter: IterableSorter):
        """
        Construct a new dict that is sorted.
        :param data: Unsorted dictionary.
        :param path: Path to current element.
        :param sorter: Sorter for iterable elements..
        """
        super().__init__(
            **{k: Sorter._sorted(data[k], path / k, sorter) for k in sorted(data.keys())}
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


class SortedIterable(list):
    """
    Replacement for a list that sorts it's keys when it is created.
    Does depth first replacement of dicts and lists so that when it sorts
    it is using the sorted version of its contents.
    """

    def __init__(self, data: Iterable, path: Path, sorter: IterableSorter):
        """
        Construct a new list that is sorted.
        :param data: Unsorted list.
        :param path: Path to the current element.
        :param sorter: Sorter for iterable elements.
        """
        super().__init__(
            sorter.sorted(
                [Sorter._sorted(v, path / f"[{i}]", sorter) for i, v in enumerate(data)], path
            )
        )

    def __lt__(self, other) -> bool:
        """
        Compare two objects.  If they are both SortedList then compare them
        as lists.  Otherwise, just compare their class types.  Order isn't
        really important.  It just needs to be consistent.
        :param other: Object to compare.
        :return: bool
        """
        if isinstance(other, SortedIterable):
            return list(self) < list(other)
        else:
            # The order doesn't really matter here as long as it is consistent.
            return str(self.__class__) < str(other.__class__)


class Sorter:
    @staticmethod
    def _sorted(
        data: NDLElement,
        path: Optional[Path] = None,
        sorter: Optional[IterableSorter] = DefaultIterableSorter(),
    ) -> Union[SortedMapping, SortedIterable, Any]:
        """
        Sort a nested dictionary/list.  Used internally to keep the path argument from being exposed in the
        public interface.
        :param data: Object to sort.
        :param path: Path to the current element.
        :param sorter: Sorter for iterable elements.
        :return: Sorted object.
        """
        path = path or Path()
        if isinstance(data, Mapping):
            return SortedMapping(data, path, sorter)
        elif isinstance(data, Iterable):
            return SortedIterable(data, path, sorter)
        else:
            return data

    @staticmethod
    def sorted(
        data: NDLElement, sorter: Optional[IterableSorter] = DefaultIterableSorter()
    ) -> Union[SortedMapping, SortedIterable, Any]:
        """
        Sort a nested dictionary/list.
        :param data: Object to sort.
        :param sorter: Sorter for iterable elements.
        :return: Sorted object.
        """
        return Sorter._sorted(data, sorter=sorter)
