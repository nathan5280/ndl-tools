"""
Normalizer used to update a leaf element so that it will compare correctly
with another NDL.  Normalizers are applied to leaf elements using
the Selector associated with the Normalizer.   Normalizers can be chained
so that they are all tried until one succeeds.
"""
import datetime
from abc import abstractmethod
from pathlib import Path
from typing import Any, Optional, List, Union

from .selector import BaseSelector, SELECTORS


class NotNormalizedError(Exception):
    """The normalizer wasn't applied to the element."""


class BaseNormalizer:
    """
    Base normalizer implements the chaining logic.
    """

    def __init__(
        self, selectors: SELECTORS = None,
    ):
        """
        Initialize the normalizer with optional parent normalizer and selector.

        :param selectors: Optional list of selector to use to select which
            elements this normalizer runs.
        """
        if selectors:
            self._selectors = selectors if isinstance(selectors, list) else [selectors]
        else:
            # No selectors specified
            self._selectors = None

    @staticmethod
    def normalize(
        element: Any, path: Path, normalizers: Optional[List["BaseNormalizer"]] = None
    ) -> Any:
        """
        Run all the normalizers until one is applied to normalize the leaf element.

        :param element: Element to normalize.
        :param path: Path to the element.
        :param normalizers: Normalizers to apply to element.
        :return: Normalized element.
        """
        if not normalizers:
            return element

        for normalizer in normalizers:
            if BaseSelector.match(path, normalizer._selectors):
                # Matched drop down and normalize the element.
                try:
                    return normalizer._normalize(element)
                except NotNormalizedError:
                    continue
        return element

    @abstractmethod
    def _normalize(self, element: Any) -> Any:
        """
        Prototype for the core normalizer logic implemented in the subclass.

        :param element: Element to normalize.
        :return: Normalized element.
        """
        pass  # pragma: no cover


NORMALIZERS = Optional[Union[BaseNormalizer, List[BaseNormalizer]]]


class DefaultNormalizer(BaseNormalizer):
    def __init__(
        self, *, selectors: SELECTORS = None,
    ):
        """
        No Op normalizer.

        :param selectors: Optional list of selector to use to select which
            elements this normalizer runs.
        """
        super().__init__(selectors)

    def _normalize(self, element: Any) -> Any:
        """No Op normalizer."""
        return element


# ToDo: Extend this to be smarter about exponential notation
#       and maybe something that adjusts based on the size or places of number being normalize.
class FloatRoundNormalizer(BaseNormalizer):
    def __init__(
        self, places: int, *, selectors: SELECTORS = None,
    ):
        """
        Round a floating point number to a set number of places.

        :param places:  Number of places to round the floating point number to.
        :param selectors: Optional slist of elector to use to select which
            elements this normalizer runs.
        """
        self._places = places
        super().__init__(selectors)

    def _normalize(self, element: Any) -> Any:
        if isinstance(element, float):
            return round(element, self._places)
        raise NotNormalizedError()


class TodayDateNormalizer(BaseNormalizer):
    def __init__(
        self, *, selectors: SELECTORS = None,
    ):
        """
        Convert all dates to today().

        :param selectors: Optional list of selector to use to select which
            elements this normalizer runs.
        """
        super().__init__(selectors)

    def _normalize(self, element: Any) -> Any:
        if isinstance(element, datetime.date):
            return datetime.date.today()
        raise NotNormalizedError


class StrTodayDateNormalizer(BaseNormalizer):
    def __init__(
        self, *, selectors: SELECTORS = None,
    ):
        """
        Overwrite string representation of a date to today().

        :param selectors: Optional list of selector to use to select which
            elements this normalizer runs.
        """
        super().__init__(selectors)

    def _normalize(self, element: Any) -> Any:
        if isinstance(element, str):
            try:
                datetime.date.fromisoformat(element)
                return datetime.date.today().isoformat()
            except ValueError:
                pass
        raise NotNormalizedError()
