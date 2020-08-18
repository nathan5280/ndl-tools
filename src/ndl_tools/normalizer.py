from abc import abstractmethod
from pathlib import Path
from typing import Any, Optional

from ndl_tools.path_matcher import BasePathMatcher, AllPathMatcher


class BaseNormalizer:
    def __init__(
        self,
        parent_normalizer: Optional["BaseNormalizer"] = None,
        path_matcher: Optional[BasePathMatcher] = None,
    ):
        self._parent_normalizer = parent_normalizer
        self._path_matcher = path_matcher or AllPathMatcher()

    def normalize(self, element: Any, path: Path) -> Any:
        if self._path_matcher.match(path):
            return self._normalize(element)
        return (
            self._parent_normalizer.normalize(element, path) if self._parent_normalizer else element
        )

    @abstractmethod
    def _normalize(self, element: Any) -> Any:
        pass


class DefaultNormalizer(BaseNormalizer):
    def __init__(
        self,
        *,
        parent_normalizer: Optional["BaseNormalizer"] = None,
        path_matcher: Optional[BasePathMatcher] = None,
    ):
        super().__init__(parent_normalizer, path_matcher)

    def _normalize(self, element: Any) -> Any:
        return element


class FloatRoundNormalizer(BaseNormalizer):
    def __init__(
        self,
        places: int,
        *,
        parent_normalizer: Optional["BaseNormalizer"] = None,
        path_matcher: Optional[BasePathMatcher] = None,
    ):
        self._places = places
        super().__init__(parent_normalizer, path_matcher)

    def _normalize(self, element: Any) -> Any:
        return round(element, self._places)
