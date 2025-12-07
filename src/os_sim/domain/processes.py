from __future__ import annotations
from dataclasses import dataclass, field
from .states import ProcessState


@dataclass(slots=True)
class Process:
    pid: int
    cpu_time: int
    mem_required: int
    remaining: int = field(init=False)
    state: ProcessState = field(default=ProcessState.READY)

    def __post_init__(self) -> None:
        self.remaining = self.cpu_time
