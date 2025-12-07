from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Sequence
from os_sim.interfaces.device import IDevice


class ITaskMigrator(ABC):
    @abstractmethod
    def rebalance(self, devices: Sequence[IDevice]) -> None:
        """
        Executes the balancing of the given devices by migrating processes.
        """
        ...
