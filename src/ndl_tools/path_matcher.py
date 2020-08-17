"""
Common PathMatchers used to determine if a Normalizer or IterableSorter will
be run on a leaf element or an Iterable.  These can be extened to create any
number of other methods for determining if the path is matched.

Matchers can be chained so that if the first matcher doesn't match successive calls
to parent matchers will be made until a match is found or all matchers have been exhausted.
"""
import re
from abc import abstractmethod
from pathlib import Path
from typing import List, Optional


class BasePathMatcher:
    """
    Base matcher for all matchers.  Implements the chaining logic.
    """

    def __init__(self, parent_matcher: Optional["BasePathMatcher"] = None):
        """
        Initialize the matcher with an optional parent matcher.

        :param parent_matcher: Parent matcher to be called if this matcher fails to match.
        """
        self._parent_matcher = parent_matcher

    def match(self, path: Path) -> bool:
        """
        Match the given path against the chain of matchers.

        :param path: Path to match.
        :return: True if matched.
        """
        if self._match(path):
            return True
        return self._parent_matcher.match(path) if self._parent_matcher else False

    @abstractmethod
    def _match(self, path: Path) -> bool:
        """
        Prototype for the core matching logic of any PathMatcher subclass.

        :param path: Path to match.
        :return: True if matched.
        """
        pass


class AllPathMatcher(BasePathMatcher):
    def __init__(self, *, parent_matcher: Optional[BasePathMatcher] = None):
        """
        Matcher that matches all paths.

        :param parent_matcher: Optional parent matcher.  Not really useful for that matcher.
        """
        super().__init__(parent_matcher)

    def _match(self, path: Path) -> bool:
        """
        Match all paths.

        :param path: Path to match.
        :return: True
        """
        return True


class ListLastComponentPathMatcher(BasePathMatcher):
    """
    Match the last component of the path against a list strings.
    """

    def __init__(self, component_names: List, *, parent_matcher: Optional[BasePathMatcher] = None):
        """
        Matcher with list of last component names to match.

        :param component_names: List of component names to match.
        :param parent_matcher: Optional parent matcher.
        """
        self._component_names = component_names
        super().__init__(parent_matcher)

    def _match(self, path: Path) -> bool:
        """
        Match the path's last component against the list of match strings.

        :param path:  Path to match.
        :return: True if matched.
        """
        return path.parts[-1] in self._component_names


class ListAnyComponentPathMatcher(BasePathMatcher):
    """
    Match any component in the path against a list of string.
    """

    def __init__(self, component_names: List, *, parent_matcher: Optional[BasePathMatcher] = None):
        """
        Matcher that matches any component of the list against a list of match strings.

        :param component_names: List of component names to match.
        :param parent_matcher: Optional parent matcher.
        """
        self._component_names = component_names
        super().__init__(parent_matcher)

    def _match(self, path: Path) -> bool:
        """
        Match the path's components against the list of match strings.

        :param path: Path to match.
        :return: True if matched.
        """
        return any((part in self._component_names for part in path.parts))


class RegExPathMatcher(BasePathMatcher):
    """
    Match the regex against the path.
    """

    def __init__(self, regex: str, parent_matcher: Optional[BasePathMatcher] = None):
        """
        Matcher that matches the path with a RegEx.

        :param regex: Regex to use to search the path.
        :param parent_matcher: Optional parent matcher.
        """
        self._regex = re.compile(regex)
        super().__init__(parent_matcher)

    def _match(self, path: Path) -> bool:
        """
        Match the path with a search for the RegEx.

        :param path: Path to match.
        :return: True if matched.
        """
        return self._regex.search(str(path)) is not None


class NegativePathMatcher(BasePathMatcher):
    """
    Matcher that inverts another matchers match results.
    """
    def __init__(
        self, path_matcher: BasePathMatcher, parent_matcher: Optional[BasePathMatcher] = None
    ):
        """
        Negate the match of the child path matcher.

        :param path_matcher: Child path matcher to negate.
        :param parent_matcher: Optional parent matcher.
        """
        self._path_matcher = path_matcher
        super().__init__(parent_matcher)

    def _match(self, path: Path) -> bool:
        """
        Negate the match result of the child.

        :param path: Path to match.
        :return: True if the path wasn't matched.
        """
        return not self._path_matcher.match(path)
