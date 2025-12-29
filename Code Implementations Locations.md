### Core Runtime

- [Operating System](src/os_sim/application/os/basic_os.py)  
- [Scheduler](src/os_sim/application/scheduling/round_robin.py)  
- [Memory Manager](src/os_sim/application/memory/simple_memory.py)  
- [Device](src/os_sim/application/devices/simple_device.py)

### Simulation Layer

- [Simulation Engine](src/os_sim/application/simulation/engine.py)  
- [TaskMigrator](src/os_sim/application/simulation/simple_migrator.py)  
- [Failure](src/os_sim/application/simulation/random_failure.py)

### Communication & Logging

- [Messaging](src/os_sim/application/ipc/simple_bus.py)  
- [Logger](src/os_sim/application/logging/in_memory_logger.py)  

### CLI / Entry Points

- [CLI main entry](src/os_sim/cli/main.py)  
- [Python launcher script](run_fakeOS.py)  

### Documentation & Diagrams

- [Architecture UML diagram](uml.svg)  