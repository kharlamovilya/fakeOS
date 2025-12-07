from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Sequence
from os_sim.interfaces.device import IDevice


class IFailureStrategy(ABC):
    @abstractmethod
    def apply(self, time: int, devices: Sequence[IDevice]) -> None:
        """
        Application of recover and failure strategy.
        """
        ...
