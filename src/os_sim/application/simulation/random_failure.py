from __future__ import annotations
from dataclasses import dataclass, field
from typing import Sequence, Dict
import random

from os_sim.interfaces.failure_strategy import IFailureStrategy
from os_sim.interfaces.device import IDevice
from os_sim.domain.states import DeviceState


@dataclass(slots=True)
class RandomFailureStrategy(IFailureStrategy):
    fail_probability: float = 0.05
    recovery_delay: int = 5
    _failed_at: Dict[int, int] = field(default_factory=dict)

    def apply(self, time: int, devices: Sequence[IDevice]) -> None:
        # try to recover failed devices
        for dev in devices:
            if dev.state is DeviceState.FAILED:
                started = self._failed_at.get(dev.id, None)
                if started is not None and time - started >= self.recovery_delay:
                    # recover
                    dev._state = DeviceState.ONLINE  # bad, change to dev.recover()
                    self._failed_at.pop(dev.id, None)

        # fail some devices
        for dev in devices:
            if dev.state is DeviceState.ONLINE and random.random() < self.fail_probability:
                dev._state = DeviceState.FAILED   # bad, change to dev.fail()
                self._failed_at[dev.id] = time
