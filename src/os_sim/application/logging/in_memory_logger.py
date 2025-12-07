from __future__ import annotations
from dataclasses import dataclass, field
from typing import List

from os_sim.interfaces.logging import IReadableLogger


@dataclass(slots=True)
class InMemoryLogger(IReadableLogger):
    _lines: List[str] = field(default_factory=list)
    _max_lines: int = 1000

    def log(self, message: str) -> None:
        self._lines.append(message)
        if len(self._lines) > self._max_lines:
            overflow = len(self._lines) - self._max_lines
            del self._lines[:overflow]

    def get_last(self, n: int = 20) -> List[str]:
        if n <= 0:
            return []
        return self._lines[-n:]
