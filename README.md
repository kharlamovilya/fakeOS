# Distributed Operating System Simulator

This project simulates behavior found in distributed operating systems. It is not an actual OS, but models major OS responsibilities so they can be studied and demonstrated.

## Overview

The simulator demonstrates how multiple independent devices cooperate to execute processes, migrate tasks, handle failures, and exchange messages. System behavior remains consistent even during failure and recovery events.

Key modeled properties:
- Multiple devices operating concurrently
- Round-robin scheduling per device
- Inter-process communication (IPC)
- Dynamic process migration between devices
- Memory tracking and capacity constraints
- Failure injection and recovery

## Non-Technical Summary

The simulator models a group of machines performing work together. Each machine:
- Receives tasks
- Has limited memory
- Executes work in time slices
- May temporarily fail
- May transfer work to other machines

This allows users to observe:
- How distributed systems balance workload
- How failure does not crash the entire system
- How communication supports coordination

## Application in Real-World Analogies

Comparable behaviors include:
- Load balancing between data centers
- Server failover during overload
- Distributed systems continuing work despite partial failures

## System Components

Each simulated device includes:
- Embedded scheduler (round-robin)
- Memory manager
- Local process table
- Inter-process communication mailbox

## Processes

Each process includes:
- PID (unique identifier)
- CPU time required
- Memory requirement
- Execution state

Possible states:
- READY  
- RUNNING  
- BLOCKED  
- MIGRATED  
- FINISHED  

## Memory Management

Per-device memory tracking includes:
- Total memory
- Used memory
- Free memory

Memory is released upon:
- Process completion
- Process migration

## Scheduling

The scheduler uses round-robin selection to ensure:
- Fair CPU allocation
- No starvation
- Predictable execution order

## Inter-Process Communication (IPC)

Communication occurs through a distributed message bus:
- Non-blocking
- Asynchronous
- Device-to-device messaging

## Process Migration

Migration occurs when a device becomes overloaded. Characteristics:
- Migration preserves remaining CPU time
- Migrated processes are removed from the original device
- The destination device accepts and executes them

## Device Failures and Recovery

Device failure is simulated probabilistically:
- Failure probability is configurable
- Devices recover automatically after a delay
- The rest of the system continues normal operation

## Command Line Interface (CLI)

The simulator provides an interactive CLI:
- Inspect system state
- Add devices
- Add processes
- Advance simulation time
  
## Command Usage

The simulator provides multiple options for controlling the environment.  
Both long and short forms of command-line arguments are supported.

### Options

| Long Option         | Short | Meaning                                                         |
|---------------------|-------|-----------------------------------------------------------------|
| `--devices N`       | `-d`  | Number of simulated devices                                     |
| `--procs N`         | `-p`  | Number of processes created at startup                          |
| `--fail X`          | `-f`  | Failure probability (0.0–1.0) for each tick                     |
| `--imbalance N`     | `-i`  | Threshold that triggers process migration between devices       |

### Example (Python Source Run)

```cmd
python run_fakeOS.py --devices 3 --procs 5 --fail 0.1 --imbalance 2
python run_fakeOS.py -d 3 -p 5 -f 0.1 -i 2
```

### Running the Executable

Unix-style terminal:

```cmd
./dist/fakeOS.exe --devices 3 --procs 5 --fail 0.1 --imbalance 2
./dist/fakeOS.exe -d 3 -p 5 -f 0.1 -i 2
```
Windows command prompt:
```cmd
dist\fakeOS.exe --devices 3 --procs 5 --fail 0.1 --imbalance 2
dist\fakeOS.exe -d 3 -p 5 -f 0.1 -i 2
```

## Architecture

The project is organized as follows:

domain/ - core models and types
interfaces/ - abstract interactions and contracts
application/ - behavioral logic and implementations
cli/ - command interaction layer

markdown
Copy code

## Design Principles

The simulator follows established design principles, including:
- Single Responsibility
- Open/Closed
- Liskov Substitution
- Interface Segregation
- Dependency Inversion

## Purpose and Use Cases

This project is appropriate for:
- Teaching distributed systems concepts
- Experimenting with scheduling and migration strategies
- Prototyping workload-balancing ideas
- Studying system resilience under failure

## Conclusion

The simulator provides a simplified but realistic model of distributed OS behavior. It enables conceptual testing, classroom demonstration, and exploratory research in a controlled environment.
