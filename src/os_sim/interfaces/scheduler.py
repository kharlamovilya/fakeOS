from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Protocol, Optional
from os_sim.domain.processes import Process


class IProcessProvider(Protocol):
    pid: int
    remaining: int
    mem_required: int


class IScheduler(ABC):
    @abstractmethod
    def add(self, proc: Process) -> None:
        ...

    @abstractmethod
    def pick_next(self) -> Optional[Process]:
        ...

    @abstractmethod
    def remove(self, proc: Process) -> None:
        ...
