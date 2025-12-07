from __future__ import annotations

import os
import time
import argparse

from os_sim.application.scheduling.round_robin import RoundRobinScheduler
from os_sim.application.memory.simple_memory import SimpleMemoryManager
from os_sim.application.os.basic_os import BasicOperatingSystem
from os_sim.application.devices.simple_device import SimpleDevice
from os_sim.application.simulation.engine import SimulationEngine
from os_sim.application.simulation.simple_migrator import SimpleTaskMigrator
from os_sim.application.simulation.random_failure import RandomFailureStrategy
from os_sim.application.logging.in_memory_logger import InMemoryLogger
from os_sim.application.ipc.simple_bus import SimpleMessageBus
from os_sim.domain.messages import Message
from typing import Callable, Sequence

from os_sim.interfaces.device import IDevice

ProcTemplate = Callable[[int], tuple[int, int]]  # (device_index) -> (cpu_time, mem)

PROC_TEMPLATES: Sequence[ProcTemplate] = [
    lambda i: (5 + i, i),
    lambda i: (5 + i, i),
    lambda i: (5 + i, i),
    lambda i: (5 + i, i),
    lambda i: (5 + i, i),
]

# === Simulation Parameters ===
IMBALANCE_THRESHOLD = 1
FAILURE_PROBABILTY = 0.1
RECOVERY_DELAY = 2

# === ANSI colors ===
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

FG_GREEN = "\033[32m"
FG_RED = "\033[31m"
FG_YELLOW = "\033[33m"
FG_CYAN = "\033[36m"
FG_MAGENTA = "\033[35m"
FG_BLUE = "\033[34m"


def color(text: str, *codes: str) -> str:
    return "".join(codes) + text + RESET


def clear_screen() -> None:
    os.system("clear||cls")
    print("Developed by <Kharlamov Ilia>")


def build_demo_simulation(
        logger: InMemoryLogger,
        num_devices: int = 2,
        procs_per_device: int = 5,
        imbalance_threshold: int = IMBALANCE_THRESHOLD,
        fail_probability: float = FAILURE_PROBABILTY,
        proc_templates: Sequence[ProcTemplate] | None = None,
) -> SimulationEngine:
    if proc_templates is None:
        proc_templates = PROC_TEMPLATES

    devices: list[SimpleDevice] = []

    # create devices
    for i in range(1, num_devices + 1):
        mem = SimpleMemoryManager(_total=20)
        sched = RoundRobinScheduler()
        os_ = BasicOperatingSystem(memory=mem, scheduler=sched, logger=logger)
        dev = SimpleDevice(_id=i, _os=os_)
        # create processes
        for k in range(procs_per_device):
            template = proc_templates[k % len(proc_templates)]
            cpu, mem_req = template(i)
            os_.create_process(cpu_time=cpu, mem_required=mem_req)

        devices.append(dev)

    bus = SimpleMessageBus(logger=logger)

    engine = SimulationEngine(
        devices=devices,
        task_migrator=SimpleTaskMigrator(imbalance_threshold=imbalance_threshold),
        failure_strategy=RandomFailureStrategy(fail_probability=fail_probability, recovery_delay=RECOVERY_DELAY),
        message_bus=bus,
        logger=logger,
    )
    return engine


def get_next_device_id(sim: SimulationEngine) -> int:
    if not sim.devices:
        return 1
    return max(d.id for d in sim.devices) + 1


def format_state(sim: SimulationEngine) -> str:
    lines: list[str] = []

    header = f"FakeOS Simulation  t={sim.time}"
    lines.append(color(header, BOLD, FG_CYAN))
    lines.append("-" * len(header))

    for dev in sim.devices:
        dev_state = dev.state.name
        if dev_state == "ONLINE":
            dev_state_str = color(dev_state, FG_GREEN, BOLD)
        else:
            dev_state_str = color(dev_state, FG_RED, BOLD)

        lines.append(f"{color('Device', FG_MAGENTA)} {dev.id}: {dev_state_str}")

        mem_mgr = dev.os().memory
        mem_total = mem_mgr.total
        mem_used = mem_mgr.used
        mem_free = mem_total - mem_used

        lines.append(
            f"  Memory: total={mem_total:03d} used={mem_used:03d} free={mem_free:03d}"
        )

        procs = list(dev.os().processes())
        if not procs:
            lines.append("  (no processes)")
        else:
            lines.append("  PID  | STATE    | REMAIN | MEM ")
            lines.append("  -----+----------+--------+-----")
            for p in procs:
                if p.state.name == "RUNNING":
                    s_color = FG_GREEN
                elif p.state.name == "READY":
                    s_color = FG_YELLOW
                elif p.state.name == "BLOCKED":
                    s_color = FG_BLUE
                elif p.state.name == "MIGRATED":
                    s_color = FG_MAGENTA
                else:
                    s_color = FG_RED

                state_text = p.state.name
                state_padded = state_text.ljust(8)

                lines.append(
                    f"  {p.pid:4d} | "
                    f"{color(state_padded, s_color)} | "
                    f"{p.remaining:6d} | "
                    f"{p.mem_required:4d}"
                )

        inbox = list(dev.os().pending_messages())
        if inbox:
            lines.append(f"  Inbox: {len(inbox)} message(s)")
        lines.append("")

    return "\n".join(lines)


def print_state(sim: SimulationEngine) -> None:
    print(format_state(sim))


def print_help() -> None:
    print(color("Commands:", BOLD))
    print("  " + color("help", FG_CYAN) + "                    - show this help")
    print("  " + color("step [N]", FG_CYAN) + "                  - advance simulation by N steps (default 1)")
    print("  " + color("run N", FG_CYAN) + "                     - same as step N")
    print("  " + color("watch N [delay]", FG_CYAN) + "           - auto-step N times with optional delay (seconds)")
    print("  " + color("state", FG_CYAN) + "                     - show current devices and processes")
    print("  " + color("send FROM TO MESSAGE...", FG_CYAN) + "   - send IPC message FROM device TO device")
    print("  " + color("add-dev MEM", FG_CYAN) + "               - add new device with MEM memory")
    print("  " + color("add-proc DEV CPU MEM", FG_CYAN) + "      - add process to device DEV")
    print("  " + color("log [N]", FG_CYAN) + "                   - show last N log lines (default 20)")
    print("  " + color("clear", FG_CYAN) + "                     - clear screen")
    print("  " + color("quit/exit", FG_CYAN) + "                 - exit console")


def find_device(sim: SimulationEngine, dev_id: int) -> IDevice | None:
    for d in sim.devices:
        if d.id == dev_id:
            return d
    return None


def repl(sim: SimulationEngine, logger: InMemoryLogger) -> None:
    print(color("FakeOS simulation console. Type 'help' for commands.", FG_CYAN))
    while True:
        try:
            raw = input(color("> ", FG_GREEN)).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if not raw:
            continue

        parts = raw.split()
        cmd = parts[0].lower()
        args = parts[1:]

        if cmd in ("quit", "exit"):
            print("Bye.")
            break

        if cmd == "help":
            print_help()
            continue

        if cmd == "clear":
            clear_screen()
            continue

        if cmd in ("step", "run"):
            n = 1
            if args:
                try:
                    n = int(args[0])
                except ValueError:
                    print("N must be an integer")
                    continue
            for _ in range(max(1, n)):
                sim.step()
            print_state(sim)
            continue

        if cmd == "watch":
            if not args:
                print("Usage: watch N [delay_seconds]")
                continue
            try:
                n = int(args[0])
            except ValueError:
                print("N must be integer")
                continue
            delay = 0.5
            if len(args) >= 2:
                try:
                    delay = float(args[1])
                except ValueError:
                    print("delay must be number (seconds)")
                    continue
            for i in range(max(1, n)):
                sim.step()
                print_state(sim)
                print(color(f"(watch {i + 1}/{n}, delay={delay}s)", DIM))
                try:
                    time.sleep(delay)
                except KeyboardInterrupt:
                    print("\nWatch interrupted.")
                    break
            continue

        if cmd == "state":
            print_state(sim)
            continue

        if cmd == "send":
            if len(args) < 3:
                print("Usage: send FROM TO MESSAGE...")
                continue
            try:
                from_id = int(args[0])
                to_id = int(args[1])
            except ValueError:
                print("FROM and TO must be integers (device ids)")
                continue
            text = " ".join(args[2:])
            if not sim.message_bus:
                print("No message bus configured.")
                continue
            msg = Message(from_device=from_id, to_device=to_id, payload=text)
            sim.message_bus.send(msg)
            print(f"Sent message from {from_id} to {to_id}")
            continue

        if cmd == "add-dev":
            if len(args) < 1:
                print("Usage: add-dev MEM")
                continue
            try:
                mem_size = int(args[0])
            except ValueError:
                print("MEM must be integer")
                continue

            dev_id = get_next_device_id(sim)
            mem = SimpleMemoryManager(_total=mem_size)
            sched = RoundRobinScheduler()
            os_ = BasicOperatingSystem(memory=mem, scheduler=sched, logger=logger)
            dev = SimpleDevice(_id=dev_id, _os=os_)
            sim.devices.append(dev)

            logger.log(f"[CMD] Added device {dev_id} with memory={mem_size}")
            print(f"Added device {dev_id} with memory={mem_size}")
            print_state(sim)
            continue

        if cmd == "add-proc":
            if len(args) < 3:
                print("Usage: add-proc DEV_ID CPU MEM")
                continue
            try:
                dev_id = int(args[0])
                cpu = int(args[1])
                mem_req = int(args[2])
            except ValueError:
                print("DEV_ID, CPU and MEM must be integers")
                continue

            dev = find_device(sim, dev_id)
            if not dev:
                print(f"No device with id={dev_id}")
                continue

            proc = dev.os().create_process(cpu_time=cpu, mem_required=mem_req)
            if proc is None:
                print(f"Cannot create process on device {dev_id}: not enough memory")
            else:
                logger.log(f"[CMD] Created process pid={proc.pid} on device {dev_id}")
                print(f"Created process pid={proc.pid} on device {dev_id}")

            print_state(sim)
            continue

        if cmd == "log":
            n = 20
            if args:
                try:
                    n = int(args[0])
                except ValueError:
                    print("N must be an integer")
                    continue
            lines = logger.get_last(n)
            print(color(f"--- Last {len(lines)} log lines ---", DIM))
            for line in lines:
                print(line)
            print(color("--- end ---", DIM))
            continue

        print(f"Unknown command: {cmd}. Type 'help'.")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Distributed OS Simulator"
    )

    parser.add_argument(
        "--devices", "-d",
        type=int,
        default=2,
        help="number of devices (default=2)"
    )

    parser.add_argument(
        "--procs", "-p",
        type=int,
        default=5,
        help="number of processes per device (default=5)"
    )

    parser.add_argument(
        "--fail", "-f",
        type=float,
        default=0.3,
        help="failure probability (default=0.3)"
    )

    parser.add_argument(
        "--imbalance", "-i",
        type=int,
        default=1,
        help="migration imbalance threshold (default=1)"
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logger = InMemoryLogger()
    sim = build_demo_simulation(
        logger=logger,
        num_devices=args.devices,
        procs_per_device=args.procs,
        imbalance_threshold=args.imbalance,
        fail_probability=args.fail,
        proc_templates=PROC_TEMPLATES,
    )
    clear_screen()
    print_state(sim)
    repl(sim, logger)


if __name__ == "__main__":
    main()
