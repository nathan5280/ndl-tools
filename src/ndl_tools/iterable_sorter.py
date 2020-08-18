from abc import abstractmethod
from pathlib import Path
from typing import Iterable, Optional

from ndl_tools.path_matcher import BasePathMatcher, AllPathMatcher


class BaseIterableSorter:
    def __init__(
        self,
        parent_sorter: Optional["BaseIterableSorter"] = None,
        path_matcher: Optional[BasePathMatcher] = None,
    ):
        self._parent_sorter = parent_sorter
        self._path_matcher = path_matcher or AllPathMatcher()

    def sorted(self, iterable: Iterable, path: Path) -> Iterable:
        if self._path_matcher.match(path):
            return self._sorted(iterable)
        return self._parent_sorter.sorted(path) if self._parent_sorter else sorted(iterable)

    @abstractmethod
    def _sorted(self, iterable: Iterable) -> Iterable:
        pass


class DefaultIterableSorter(BaseIterableSorter):
    def __init__(
        self,
        *,
        parent_sorter: Optional[BaseIterableSorter] = None,
        path_matcher: Optional[BasePathMatcher] = None,
    ):
        super().__init__(parent_sorter, path_matcher)

    def _sorted(self, iterable: Iterable) -> Iterable:
        return sorted(iterable)


class NoSortIterableSorter(BaseIterableSorter):
    def __init__(
        self,
        *,
        parent_sorter: Optional[BaseIterableSorter] = None,
        path_matcher: Optional[BasePathMatcher] = None,
    ):
        super().__init__(parent_sorter, path_matcher)

    def _sorted(self, iterable: Iterable) -> Iterable:
        return iterable
