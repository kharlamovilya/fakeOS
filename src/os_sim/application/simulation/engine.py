from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional

from os_sim.interfaces.device import IDevice
from os_sim.interfaces.task_migrator import ITaskMigrator
from os_sim.interfaces.failure_strategy import IFailureStrategy
from os_sim.interfaces.ipc import IMessageBus
from os_sim.interfaces.logging import ILogger


@dataclass(slots=True)
class SimulationEngine:
    devices: List[IDevice]
    task_migrator: Optional[ITaskMigrator] = None
    failure_strategy: Optional[IFailureStrategy] = None
    message_bus: Optional[IMessageBus] = None
    logger: Optional[ILogger] = None

    time: int = 0

    def step(self) -> None:
        self.time += 1
        if self.logger:
            self.logger.log(f"[SIM] === Step t={self.time} ===")

        if self.failure_strategy:
            self.failure_strategy.apply(self.time, self.devices)

        # pass msgs
        if self.message_bus:
            for d in self.devices:
                inbox = self.message_bus.poll_for_device(d.id)
                if inbox:
                    d.os().deliver_messages(inbox)

        # tick devices
        for d in self.devices:
            d.tick()

        # migrate tasks
        if self.task_migrator:
            self.task_migrator.rebalance(self.devices)
