from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List


class ILogger(ABC):
    """Simple logging interface"""

    @abstractmethod
    def log(self, message: str) -> None:
        ...


class IReadableLogger(ILogger, ABC):
    """Logger extension for reading logs."""

    @abstractmethod
    def get_last(self, n: int = 20) -> List[str]:
        ...
