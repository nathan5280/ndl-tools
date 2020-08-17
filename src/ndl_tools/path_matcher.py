"""
Common PathMatchers used to determine if a Normalizer or IterableSorter will
be run on a leaf element or an Iterable.  These can be extened to create any
number of other methods for determining if the path is matched.


"""
import re
from abc import abstractmethod
from pathlib import Path
from typing import List, Optional


class BasePathMatcher:
    def __init__(self, parent_matcher: Optional["BasePathMatcher"] = None):
        self._parent_matcher = parent_matcher

    @abstractmethod
    def match(self, path: Path) -> bool:
        pass

    def parent_match(self, path: Path) -> bool:
        return self._parent_matcher.match(path) if self._parent_matcher else False


class ListLastComponentPathMatcher(BasePathMatcher):
    def __init__(self, component_names: List, *, parent_matcher: Optional[BasePathMatcher] = None):
        self._component_names = component_names
        super().__init__(parent_matcher)

    def match(self, path: Path) -> bool:
        if path.parts[-1] in self._component_names:
            return True
        return self.parent_match(path)


class ListAnyComponentPathMatcher(BasePathMatcher):
    def __init__(self, component_names: List, *, parent_matcher: Optional[BasePathMatcher] = None):
        self._component_names = component_names
        super().__init__(parent_matcher)

    def match(self, path: Path) -> bool:
        if any((part in self._component_names for part in path.parts)):
            return True
        return self.parent_match(path)


class RegExPathMatcher(BasePathMatcher):
    def __init__(self, regex: str, parent_matcher: Optional[BasePathMatcher] = None):
        self._regex = re.compile(regex)
        super().__init__(parent_matcher)

    def match(self, path: Path) -> bool:
        if self._regex.search(str(path)) is not None:
            return True
        return self.parent_match(path)
