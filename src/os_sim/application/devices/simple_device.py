from __future__ import annotations
from dataclasses import dataclass
from os_sim.domain.states import DeviceState
from os_sim.interfaces.device import IDevice
from os_sim.interfaces.operating_system import IOperatingSystem


@dataclass(slots=True)
class SimpleDevice(IDevice):
    _id: int
    _os: IOperatingSystem
    _state: DeviceState = DeviceState.ONLINE

    @property
    def id(self) -> int:
        return self._id

    @property
    def state(self) -> DeviceState:
        return self._state

    def os(self) -> IOperatingSystem:
        return self._os

    def tick(self) -> None:
        if self._state is DeviceState.ONLINE:
            self._os.tick()

    def is_alive(self) -> bool:
        return self._state is DeviceState.ONLINE
