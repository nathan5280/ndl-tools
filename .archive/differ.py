from pathlib import Path
from typing import Union, Iterable, Mapping, Optional, Callable, Any

NDL = Union[Mapping, Iterable]


class DifferError(Exception):
    """General error related to the set operation."""


def no_op_sorter(path: Path, list_: Iterable) -> Iterable:
    return list_


def no_op_normalizer(path: Path, obj: Any) -> Any:
    return obj


class DiffResult:
    def __init__(self, match: bool, diff: Union[NDL, None]):
        self._match = match
        self.diff = diff

    def __bool__(self) -> bool:
        return self._match


def _mapping_difference(
    path: Path,
    left: NDL,
    right: NDL,
    list_sorter: Optional[Callable[[Path], Iterable]] = no_op_sorter,
    normalizer: Optional[Callable[[Path], Any]] = no_op_normalizer,
) -> DiffResult:
    diff = dict()
    for k, v in left.items():
        if k in right:
            result = _dispatch(path / str(k), v, None, list_sorter, normalizer)



def _iterable_difference(
    path: Path,
    left: NDL,
    right: NDL,
    list_sorter: Optional[Callable[[Path], Iterable]] = no_op_sorter,
    normalizer: Optional[Callable[[Path], Any]] = no_op_normalizer,
) -> DiffResult:
    for i, v in enumerate(left):
        _dispatch(path / f"[{i}]", v, None, list_sorter, normalizer)


def _dispatch(
    path: Path,
    left: NDL,
    right: NDL,
    list_sorter: Optional[Callable[[Path], Iterable]] = no_op_sorter,
    normalizer: Optional[Callable[[Path], Any]] = no_op_normalizer,
) -> DiffResult:
    if isinstance(left, Mapping):
        return _mapping_difference(path, left, right, list_sorter, normalizer)
    if isinstance(left, Iterable):
        return _iterable_difference(path, left, right, list_sorter, normalizer)
    print(path, left)
    return DiffResult(left == right, None)


def difference(
    left: NDL,
    right: NDL,
    list_sorter: Optional[Callable[[Path], Iterable]] = no_op_sorter,
    normalizer: Optional[Callable[[Path], Any]] = no_op_normalizer,
) -> DiffResult:
    return _dispatch(Path(), left, right, list_sorter, normalizer)
