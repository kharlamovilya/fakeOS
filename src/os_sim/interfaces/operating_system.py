from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, Iterable

from os_sim.domain.processes import Process
from os_sim.domain.messages import Message


class IOperatingSystem(ABC):
    def __init__(self):
        self.memory = None

    @abstractmethod
    def create_process(self, cpu_time: int, mem_required: int) -> Optional[Process]:
        ...

    @abstractmethod
    def tick(self) -> None:
        ...

    @abstractmethod
    def processes(self) -> Iterable[Process]:
        ...

    @abstractmethod
    def deliver_messages(self, messages: Iterable[Message]) -> None:
        ...

    @abstractmethod
    def pending_messages(self) -> Iterable[Message]:
        ...
