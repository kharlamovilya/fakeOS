from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
from os_sim.domain.processes import Process
from os_sim.interfaces.scheduler import IScheduler


@dataclass(slots=True)
class RoundRobinScheduler(IScheduler):
    _queue: List[Process] = field(default_factory=list)

    def add(self, proc: Process) -> None:
        self._queue.append(proc)

    def pick_next(self) -> Optional[Process]:
        if not self._queue:
            return None
        proc = self._queue.pop(0)
        self._queue.append(proc)
        return proc

    def remove(self, proc: Process) -> None:
        if proc in self._queue:
            self._queue.remove(proc)
