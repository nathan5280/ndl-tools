"""
Common Selectors used to determine if a Normalizer or ListSorter will
be run on a leaf element or an List.  These can be extened to create any
number of other methods for determining if the path is matched.

Selectorss can be chained so that if the first selector doesn't match successive calls
to parent selectors will be made until a match is found or all selectors have been exhausted.
"""
import re
from abc import abstractmethod
from pathlib import Path
from typing import List, Optional


class BaseSelector:
    """
    Base path selector implements the chaining logic.
    """

    def __init__(self, parent_selector: Optional["BaseSelector"] = None):
        """
        Initialize the selector with an optional parent selector.

        :param parent_selector: Parent selector to be called if this selector fails to match.
        """
        self._parent_selector = parent_selector

    def match(self, path: Path) -> bool:
        """
        Match the given path against the chain of selectors.

        :param path: Path to match.
        :return: True if matched.
        """
        if self._match(path):
            return True
        return self._parent_selector.match(path) if self._parent_selector else False

    @abstractmethod
    def _match(self, path: Path) -> bool:
        """
        Prototype for the core matching logic of any PathSelectors subclass.

        :param path: Path to match.
        :return: True if matched.
        """
        pass


class AllSelector(BaseSelector):
    def __init__(self, *, parent_selector: Optional[BaseSelector] = None):
        """
        Selectors that matches all paths.

        :param parent_selector: Optional parent selector.  Not really useful for that selector.
        """
        super().__init__(parent_selector)

    def _match(self, path: Path) -> bool:
        """
        Match all paths.

        :param path: Path to match.
        :return: True
        """
        return True


class ListLastComponentSelector(BaseSelector):
    """
    Match the last component of the path against a list strings.
    """

    def __init__(self, component_names: List, *, parent_selector: Optional[BaseSelector] = None):
        """
        Selectors with list of last component names to match.

        :param component_names: List of component names to match.
        :param parent_selector: Optional parent selector.
        """
        self._component_names = component_names
        super().__init__(parent_selector)

    def _match(self, path: Path) -> bool:
        """
        Match the path's last component against the list of match strings.

        :param path:  Path to match.
        :return: True if matched.
        """
        return path.parts[-1] in self._component_names


class ListAnyComponentSelector(BaseSelector):
    """
    Match any component in the path against a list of string.
    """

    def __init__(self, component_names: List, *, parent_selector: Optional[BaseSelector] = None):
        """
        Selectors that matches any component of the list against a list of match strings.

        :param component_names: List of component names to match.
        :param parent_selector: Optional parent selector.
        """
        self._component_names = component_names
        super().__init__(parent_selector)

    def _match(self, path: Path) -> bool:
        """
        Match the path's components against the list of match strings.

        :param path: Path to match.
        :return: True if matched.
        """
        return any((part in self._component_names for part in path.parts))


class RegExSelector(BaseSelector):
    """
    Match the regex against the path.
    """

    def __init__(self, regex: str, parent_selector: Optional[BaseSelector] = None):
        """
        Selectors that matches the path with a RegEx.

        :param regex: Regex to use to search the path.
        :param parent_selector: Optional parent selector.
        """
        self._regex = re.compile(regex)
        super().__init__(parent_selector)

    def _match(self, path: Path) -> bool:
        """
        Match the path with a search for the RegEx.

        :param path: Path to match.
        :return: True if matched.
        """
        return self._regex.search(str(path)) is not None


class NegativeSelector(BaseSelector):
    """
    Selectors that inverts another selectors match results.
    """
    def __init__(
        self, selector: BaseSelector, parent_selector: Optional[BaseSelector] = None
    ):
        """
        Negate the match of the child path selector.

        :param selector: Child path selector to negate.
        :param parent_selector: Optional parent selector.
        """
        self._selector = selector
        super().__init__(parent_selector)

    def _match(self, path: Path) -> bool:
        """
        Negate the match result of the child.

        :param path: Path to match.
        :return: True if the path wasn't matched.
        """
        return not self._selector.match(path)
