from __future__ import annotations
from abc import ABC, abstractmethod
from os_sim.domain.states import DeviceState
from .operating_system import IOperatingSystem


class IDevice(ABC):
    @property
    @abstractmethod
    def id(self) -> int:
        ...

    @property
    @abstractmethod
    def state(self) -> DeviceState:
        ...

    @abstractmethod
    def os(self) -> IOperatingSystem:
        ...

    @abstractmethod
    def tick(self) -> None:
        ...

    @abstractmethod
    def is_alive(self) -> bool:
        """Удобный шорткат — «онлайн ли девайс»."""
        ...
