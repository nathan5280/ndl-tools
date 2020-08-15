"""
Sort nested dictionary/lists.  The sort order isn't really important,
just that it is consistent.
"""
from typing import Any, Union, Mapping, Iterable

NDLElement = Union[Mapping, Iterable, Any]


class SortedMapping(dict):
    """
    Replacement for a dictionary that sorts it's keys when it is created.
    Does depth first replacement of dicts and lists so that when it sorts
    it is using the sorted version of its contents.
    """

    def __init__(self, data: Mapping):
        """
        Construct a new dict that is sorted.
        :param data: Unsorted dictionary.
        """
        super().__init__(**{k: Sorter.sorted(data[k]) for k in sorted(data.keys())})

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

    def __init__(self, data: Iterable):
        """
        Construct a new list that is sorted.
        :param data: Unsorted list.
        """
        super().__init__(sorted([Sorter.sorted(v) for v in data]))

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
    def sorted(data: NDLElement) -> Union[SortedMapping, SortedIterable, Any]:
        """
        Sort a nested dictionary/list.
        :param data: Object to sort.
        :return: Sorted object.
        """
        if isinstance(data, Mapping):
            return SortedMapping(data)
        elif isinstance(data, Iterable):
            return SortedIterable(data)
        else:
            return data
