"""
Normalizer used to update a leaf element so that it will compare correctly
with another NDL.  Normalizers are applied to leaf elements using
the Selector associated with the Normalizer.   Normalizers can be chained
so that they are all tried until one succeeds.
"""
import datetime
from abc import abstractmethod
from pathlib import Path
from typing import Any, Optional

from .selector import BaseSelector, AllSelector


class NotNormalizedError(Exception):
    """The normalizer wasn't applied to the element."""


class BaseNormalizer:
    """
    Base normalizer implements the chaining logic.
    """

    def __init__(
        self,
        parent_normalizer: Optional["BaseNormalizer"] = None,
        selector: Optional[BaseSelector] = None,
    ):
        """
        Initialize the normalizer with optional parent normalizer and selector.

        :param parent_normalizer: Optional parent normalizer to run if this normalizer
            isn't selected by the selector.
        :param selector: Optional selector to use to select which
            elements this normalizer runs.
        """
        self._parent_normalizer = parent_normalizer
        self._selector = selector or AllSelector()

    def normalize(self, element: Any, path: Path) -> Any:
        """
        Run all the normalizers until one is applied to normalize the leaf element.

        :param element: Element to normalize.
        :param path: Path to the element.
        :return: Normalized element.
        """

        if self._selector.match(path):
            try:
                return self._normalize(element)
            except NotNormalizedError:
                pass
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
        selector: Optional[BaseSelector] = None,
    ):
        """
        No Op normalizer.

        :param parent_normalizer: Optional parent normalizer to run if this normalizer
            isn't selected by the selector.
        :param selector: Optional selector to use to select which
            elements this normalizer runs.
        """
        super().__init__(parent_normalizer, selector)

    def _normalize(self, element: Any) -> Any:
        """No Op normalizer."""
        return element


# ToDo: Extend this to be smarter about exponential notation
#       and maybe something that adjusts based on the size or places of number being normalize.
class FloatRoundNormalizer(BaseNormalizer):
    def __init__(
        self,
        places: int,
        *,
        parent_normalizer: Optional["BaseNormalizer"] = None,
        selector: Optional[BaseSelector] = None,
    ):
        """
        Round a floating point number to a set number of places.

        :param places:  Number of places to round the floating point number to.
        :param parent_normalizer: Optional parent normalizer to run if this normalizer
            isn't selected by the selector.
        :param selector: Optional selector to use to select which
            elements this normalizer runs.
        """
        self._places = places
        super().__init__(parent_normalizer, selector)

    def _normalize(self, element: Any) -> Any:
        if isinstance(element, float):
            return round(element, self._places)
        raise NotNormalizedError()


class TodayDateNormalizer(BaseNormalizer):
    def __init__(
        self,
        *,
        parent_normalizer: Optional["BaseNormalizer"] = None,
        selector: Optional[BaseSelector] = None,
    ):
        """
        Convert all dates to today().

        :param parent_normalizer: Optional parent normalizer to run if this normalizer
            isn't selected by the selector.
        :param selector: Optional selector to use to select which
            elements this normalizer runs.
        """
        super().__init__(parent_normalizer, selector)

    def _normalize(self, element: Any) -> Any:
        if isinstance(element, datetime.date):
            return datetime.date.today()
        raise NotNormalizedError


class StrTodayDateNormalizer(BaseNormalizer):
    def __init__(
        self,
        *,
        parent_normalizer: Optional["BaseNormalizer"] = None,
        selector: Optional[BaseSelector] = None,
    ):
        """
        Overwrite string representation of a date to today().

        :param parent_normalizer: Optional parent normalizer to run if this normalizer
            isn't selected by the selector.
        :param selector: Optional selector to use to select which
            elements this normalizer runs.
        """
        super().__init__(parent_normalizer, selector)

    def _normalize(self, element: Any) -> Any:
        if isinstance(element, str):
            try:
                datetime.date.fromisoformat(element)
                return datetime.date.today().isoformat()
            except ValueError:
                pass
        raise NotNormalizedError()
