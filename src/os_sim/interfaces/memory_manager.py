from __future__ import annotations
from abc import ABC, abstractmethod


class IMemoryManager(ABC):
    @abstractmethod
    def can_alloc(self, amount: int) -> bool:
        ...

    @abstractmethod
    def alloc(self, amount: int) -> bool:
        ...

    @abstractmethod
    def free(self, amount: int) -> None:
        ...

    @property
    @abstractmethod
    def total(self) -> int:
        ...

    @property
    @abstractmethod
    def used(self) -> int:
        ...
