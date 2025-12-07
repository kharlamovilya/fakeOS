from __future__ import annotations
from dataclasses import dataclass
from os_sim.interfaces.memory_manager import IMemoryManager


@dataclass(slots=True)
class SimpleMemoryManager(IMemoryManager):
    _total: int
    _used: int = 0

    def can_alloc(self, amount: int) -> bool:
        return self._used + amount <= self._total

    def alloc(self, amount: int) -> bool:
        if not self.can_alloc(amount):
            return False
        self._used += amount
        return True

    def free(self, amount: int) -> None:
        self._used = max(0, self._used - amount)

    @property
    def total(self) -> int:
        return self._total

    @property
    def used(self) -> int:
        return self._used
