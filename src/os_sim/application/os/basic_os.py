from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Iterable

from os_sim.domain.processes import Process
from os_sim.domain.states import ProcessState
from os_sim.domain.messages import Message
from os_sim.interfaces.operating_system import IOperatingSystem
from os_sim.interfaces.scheduler import IScheduler
from os_sim.interfaces.memory_manager import IMemoryManager
from os_sim.interfaces.logging import ILogger


@dataclass(slots=True)
class BasicOperatingSystem(IOperatingSystem):
    memory: IMemoryManager
    scheduler: IScheduler

    logger: ILogger | None = None

    _processes: List[Process] = field(default_factory=list)
    _current: Optional[Process] = None
    _next_pid: int = 1
    _inbox: List[Message] = field(default_factory=list)

    # ---- API IOperatingSystem ----

    def create_process(self, cpu_time: int, mem_required: int) -> Optional[Process]:
        if not self.memory.alloc(mem_required):
            if self.logger:
                self.logger.log(
                    f"[OS] Cannot allocate memory for new process "
                    f"(cpu_time={cpu_time}, mem={mem_required})"
                )
            return None

        p = Process(pid=self._next_pid, cpu_time=cpu_time, mem_required=mem_required)
        self._next_pid += 1

        self._processes.append(p)
        self.scheduler.add(p)

        if self.logger:
            self.logger.log(
                f"[OS] Created process pid={p.pid}, cpu_time={p.cpu_time}, "
                f"mem={p.mem_required}"
            )

        return p

    def processes(self) -> Iterable[Process]:
        return tuple(self._processes)

    def _pick_new_current(self) -> None:
        self._current = self.scheduler.pick_next()
        if self._current:
            self._current.state = ProcessState.RUNNING

    def tick(self) -> None:
        # check income msg
        if self._inbox and self.logger:
            self.logger.log(f"[OS] Processing {len(self._inbox)} incoming messages")
            self._inbox.clear()

        # if current proc is FINISHED, pick a new one
        if self._current is None or self._current.state is ProcessState.FINISHED:
            self._pick_new_current()

        if not self._current:
            # remove dead procs
            self._cleanup_finished()
            return  # idle

        # execute current proc
        self._current.remaining -= 1

        if self._current.remaining <= 0:
            self._current.state = ProcessState.FINISHED
            if self.logger:
                self.logger.log(f"[OS] Process pid={self._current.pid} finished")
            self._current = None

        # remove FINISHED procs
        self._cleanup_finished()

    def deliver_messages(self, messages: Iterable[Message]) -> None:
        msgs = list(messages)
        if not msgs:
            return
        self._inbox.extend(msgs)
        if self.logger:
            self.logger.log(f"[OS] Received {len(msgs)} messages")

    def pending_messages(self) -> Iterable[Message]:
        return tuple(self._inbox)

    def _cleanup_finished(self) -> None:
        if not self._processes:
            return

        alive: list[Process] = []
        for p in self._processes:
            if p.state in (ProcessState.FINISHED, ProcessState.MIGRATED):
                self.scheduler.remove(p)
                self.memory.free(p.mem_required)
                if self.logger:
                    self.logger.log(
                        f"[OS] Reaped {p.state.name.lower()} process pid={p.pid}, "
                        f"mem={p.mem_required}"
                    )
            else:
                alive.append(p)

        self._processes = alive
