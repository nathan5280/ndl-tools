from abc import abstractmethod
from pathlib import Path
from typing import Any


class BaseNormalizer:
    @abstractmethod
    def normalize(self, element: Any, path: Path) -> Any:
        pass


class FloatRoundNormalizer(BaseNormalizer):
    def __init__(self, places: int):
        self._places = places

    def normalize(self, element: Any, path: Path) -> Any:
        if isinstance(element, float):
            return round(element, self._places)
        return element
