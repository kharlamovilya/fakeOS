from __future__ import annotations
from enum import Enum, auto


class ProcessState(Enum):
    READY = auto()
    RUNNING = auto()
    BLOCKED = auto()
    FINISHED = auto()
    MIGRATED = auto()

class DeviceState(Enum):
    ONLINE = auto()
    FAILED = auto()
