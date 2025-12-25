from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence, Optional

from os_sim.domain.states import ProcessState
from os_sim.interfaces.task_migrator import ITaskMigrator
from os_sim.interfaces.device import IDevice
from os_sim.domain.processes import Process


@dataclass(slots=True)
class SimpleTaskMigrator(ITaskMigrator):
    imbalance_threshold: int = 2

    def rebalance(self, devices: Sequence[IDevice]) -> None:
        if len(devices) < 2:
            return

        loads = [
            (
                dev,
                sum(
                    1 for p in dev.os().processes()
                    if p.state.name in ("READY", "RUNNING")
                ),
            )
            for dev in devices
            if dev.is_alive()
        ]
        if not loads:
            return

        most_loaded, max_load = max(loads, key=lambda x: x[1])
        least_loaded, min_load = min(loads, key=lambda x: x[1])

        if max_load - min_load < self.imbalance_threshold:
            return

        proc_to_move: Optional[Process] = None
        for p in most_loaded.os().processes():
            if p.state.name in ("READY", "RUNNING"):
                proc_to_move = p
                break

        if not proc_to_move:
            return

        target_os = least_loaded.os()
        new_proc = target_os.create_process(
            cpu_time=proc_to_move.remaining,
            mem_required=proc_to_move.mem_required,
        )
        if not new_proc:
            # no memory to allocate for new proc
            return
        cpu_time = proc_to_move.remaining
        proc_to_move.remaining = 0
        proc_to_move.state = ProcessState.MIGRATED

        os_logger = getattr(most_loaded.os(), "logger", None)
        if os_logger:
            os_logger.log(
                f"[MIGRATION] moved pid={proc_to_move.pid} with cpu_time={cpu_time} "
                f"from device {most_loaded.id} to device {least_loaded.id} "
                f"(new pid={new_proc.pid})"
            )
