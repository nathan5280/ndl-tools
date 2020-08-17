from abc import abstractmethod
from pathlib import Path
from typing import Iterable, List


class BaseIterableSorter:
    @abstractmethod
    def sorted(self, iterable: Iterable, path: Path) -> Iterable:
        pass


class DefaultIterableSorter(BaseIterableSorter):
    def sorted(self, iterable: Iterable, path: Path) -> Iterable:
        return sorted(iterable)


class NoSortIterableSorter(BaseIterableSorter):
    def __init__(self, no_sort_names: List[str]):
        self._no_sort_names = no_sort_names

    def sorted(self, iterable: Iterable, path: Path) -> Iterable:
        if path.parts[-1] in self._no_sort_names:
            return iterable
        return sorted(iterable)


