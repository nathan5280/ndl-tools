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
from typing import List, Optional, Union


class BaseSelector:
    """
    Base path selector implements the chaining logic.
    """

    def __init__(self):
        """
        Initialize the selector.
        """

    @staticmethod
    def match(path: Path, selectors: Optional[List["BaseSelector"]] = None) -> bool:
        """
        Match the given path against the chain of selectors.

        :param path: Path to match.
        :param selectors: List of selectors.
        :return: True if matched.
        """
        if not selectors:
            return True

        for selector in selectors:
            if selector._match(path):
                return True
        return False

    @abstractmethod
    def _match(self, path: Path) -> bool:
        """
        Prototype for the core matching logic of any PathSelectors subclass.

        :param path: Path to match.
        :return: True if matched.
        """
        pass  # pragma: no cover


SELECTORS = Optional[Union[BaseSelector, List[BaseSelector]]]


class ListLastComponentSelector(BaseSelector):
    """
    Match the last component of the path against a list strings.
    """

    def __init__(self, component_names: List):
        """
        Selector with list of last component names to match.

        :param component_names: List of component names to match.
        """
        self._component_names = component_names
        super().__init__()

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

    def __init__(self, component_names: List):
        """
        Selectors that matches any component of the list against a list of match strings.

        :param component_names: List of component names to match.
        """
        self._component_names = component_names
        super().__init__()

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

    def __init__(self, regex: str):
        """
        Selectors that matches the path with a RegEx.

        :param regex: Regex to use to search the path.
        """
        self._regex = re.compile(regex)
        super().__init__()

    def _match(self, path: Path) -> bool:
        """
        Match the path with a search for the RegEx.

        :param path: Path to match.
        :return: True if matched.
        """
        return self._regex.search(str(path)) is not None


class NegativeSelector(BaseSelector):
    """
    Selector that inverts another selectors match results.
    """

    def __init__(self, selector: BaseSelector):
        """
        Negate the match of the child path selector.

        :param selector: Child path selector to negate.
        """
        self._selector = selector
        super().__init__()

    def _match(self, path: Path) -> bool:
        """
        Negate the match result of the child.

        :param path: Path to match.
        :return: True if the path wasn't matched.
        """
        return not self._selector.match(path, [self._selector])
