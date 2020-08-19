"""
Normalizer used to update a leaf element so that it will compare correctly
with another NDL.  Normalizers are applied to leaf elements using
the PathMatcher associated with the Normalizer.   Normalizers can be chained
so that they are all tried until one succeeds.
"""
import datetime
from abc import abstractmethod
from pathlib import Path
from typing import Any, Optional

from ndl_tools.path_matcher import BasePathMatcher, AllPathMatcher


class BaseNormalizer:
    """
    Base normalizer implements the chaining logic.
    """
    def __init__(
        self,
        parent_normalizer: Optional["BaseNormalizer"] = None,
        path_matcher: Optional[BasePathMatcher] = None,
    ):
        """
        Initialize the normalizer with optional parent normalizer and path matcher.

        :param parent_normalizer: Optional parent normalizer to run if this normalizer
            isn't selected by the path matcher.
        :param path_matcher: Optional path matcher to use to select which
            elements this normalizer runs.
        """
        self._parent_normalizer = parent_normalizer
        self._path_matcher = path_matcher or AllPathMatcher()

    def normalize(self, element: Any, path: Path) -> Any:
        """
        Run all the normalizers until one is applied to normalize the leaf element.

        :param element: Element to normalize.
        :param path: Path to the element.
        :return: Normalized element.
        """

        # ToDo: Need to know to call parent normalizer.
        #       _normalize() raise exception?
        #       _normalize() call parent normalize()?
        if self._path_matcher.match(path):
            return self._normalize(element)
        return (
            self._parent_normalizer.normalize(element, path) if self._parent_normalizer else element
        )

    @abstractmethod
    def _normalize(self, element: Any) -> Any:
        """
        Prototype for the core normalizer logic implemented in the subclass.

        :param element: Element to normalize.
        :return: Normalized element.
        """
        pass


class DefaultNormalizer(BaseNormalizer):
    def __init__(
        self,
        *,
        parent_normalizer: Optional["BaseNormalizer"] = None,
        path_matcher: Optional[BasePathMatcher] = None,
    ):
        """
        No Op normalizer.

        :param parent_normalizer: Optional parent normalizer to run if this normalizer
            isn't selected by the path matcher.
        :param path_matcher: Optional path matcher to use to select which
            elements this normalizer runs.
        """
        super().__init__(parent_normalizer, path_matcher)

    def _normalize(self, element: Any) -> Any:
        """No Op normalizer."""
        return element


class FloatRoundNormalizer(BaseNormalizer):
    def __init__(
        self,
        places: int,
        *,
        parent_normalizer: Optional["BaseNormalizer"] = None,
        path_matcher: Optional[BasePathMatcher] = None,
    ):
        """
        Round a floating point number to a set number of places.

        :param places:  Number of places to round the floating point number to.
        :param parent_normalizer: Optional parent normalizer to run if this normalizer
            isn't selected by the path matcher.
        :param path_matcher: Optional path matcher to use to select which
            elements this normalizer runs.
        """
        self._places = places
        super().__init__(parent_normalizer, path_matcher)

    def _normalize(self, element: Any) -> Any:
        if isinstance(element, float):
            return round(element, self._places)
        return element


class TodayDateNormalizer(BaseNormalizer):
    def __init__(
        self,
        *,
        parent_normalizer: Optional["BaseNormalizer"] = None,
        path_matcher: Optional[BasePathMatcher] = None,
    ):
        """
        Convert all dates to today().

        :param parent_normalizer: Optional parent normalizer to run if this normalizer
            isn't selected by the path matcher.
        :param path_matcher: Optional path matcher to use to select which
            elements this normalizer runs.
        """
        super().__init__(parent_normalizer, path_matcher)

    def _normalize(self, element: Any) -> Any:
        if isinstance(element, datetime.date):
            return datetime.date.today()
        return element
