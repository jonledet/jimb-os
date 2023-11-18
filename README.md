Built Using Python 3.11.2
# CPU Scheduling Simulation Program (jimb-os)

# Table of Contents

1. [Process Class Documentation](#process-class-documentation)
   
2. [Scheduler Class Documentation](#scheduler-class-documentation)
   
3. [CPU Class Documentation](#cpu-class-documentation)
   
4. [Memory Class Documentation](#memory-class-documentation)
   
5. [Main Class Documentation](#main-class-documentation)

## Process Class Documentation

### Overview
The `Process` class represents a process to be executed by the CPU simulator. It reads data from a text file containing assembly-like instructions and an arrival time, calculates process metrics, and tracks execution status.

### Attributes
- `pid`: Unique identifier (integer) for the process.
- `filename`: Name of the file containing process data.
- `arrival_time`: Arrival time (integer) of the process.
- `code`: Dictionary with integer keys as instruction addresses and values as lists representing instructions.
- `executed_burst_time`: Time spent executing the process.
- `initial_burst_time`: Initial burst time of the process.
- `burst_time`: Burst time of the process.
- `remaining_time`: Remaining time needed for process completion.
- `waiting_time`: Waiting time of the process.
- `turnaround_time`: Turnaround time of the process.
- `response_time`: Response time of the process.
- `execution_status`: Boolean indicating if the process has finished execution.

### Methods
- `__init__(self, pid, filename)`: Initializes a `Process` object with a given process identifier and process data file name.
- `read_process_data(self)`: Reads process data from the specified file, parses arrival time and code, and stores parsed code in the `code` attribute.

## Scheduler Class Documentation

### Overview
The `Scheduler` class manages process execution using different scheduling algorithms (FCFS, RR, SPN, SRT). It provides methods for adding processes, computing burst times, running algorithms, recording CPU activity, calculating metrics, and visualizing activity.

### Attributes
- `memory`: Memory object used by the scheduler.
- `ready_queue`: Deque holding processes ready for execution.
- `process_list`: List of all processes added to the scheduler.
- `cpu_activity_log`: Pandas DataFrame storing CPU activity log.

### Methods
- `__init__(self, memory)`: Initializes a `Scheduler` object with a given memory object and empty attributes.
- `add_process(self, process)`: Adds a process object to the `process_list`.
- `compute_burst_times(self, cpu)`: Computes burst times for processes in the `process_list` using the given CPU object.
- `run_FCFS(self, cpu)`: Runs the FCFS scheduling algorithm using the given CPU object.
- `run_RR(self, cpu, time_quantum)`: Runs the RR scheduling algorithm using the given CPU object and specified time quantum.
- `run_SPN(self, cpu)`: Runs the SPN scheduling algorithm using the given CPU object.
- `run_SRT(self, cpu)`: Runs the SRT scheduling algorithm using the given CPU object.
- `record_cpu_activity(self, pid, start_time, end_time)`: Records CPU activity with process ID, start time, and end time.
- `calculate_performance_metrics(self)`: Calculates performance metrics for processes.
- `display_performance_metrics_table(self, performance_metrics, algorithm_name, time_quantum=None)`: Displays a table of performance metrics.
- `visualize_cpu_activity(self, algorithm_name, time_quantum=None)`: Visualizes CPU activity using a Gantt chart.

## CPU Class Documentation

### Overview
The `CPU` class represents a simple CPU simulator with a basic instruction set for executing processes with assembly-like instructions.

### Attributes
- `global_clock`: Class-level attribute tracking the global clock.
- `registers`: List of 16 integer registers.
- `program_counter`: Integer tracking the current instruction.
- `cache`: Cache for temporarily storing preempted processes.
- `memory`: Dictionary representing memory address space.

### Methods
- `__init__(self)`: Initializes a `CPU` object with registers, program counter, cache, and empty memory.
- `execute_instruction(self, instruction, simulate=False)`: Executes a single instruction provided as a tuple.
- `execute_process(self, process, time_quantum=None, check_preempt=None, simulate=False)`: Executes a process with optional parameters.
- `store_preempted_process(self, process)`: Stores a preempted process in the cache.

## Memory Class Documentation

### Overview
The `Memory` class represents a simple memory management system that allocates and deallocates memory frames for processes.

### Attributes
- `page_table`: Dictionary mapping process IDs to frame indices.
- `physical_memory`: List of memory frames.

### Methods
- `__init__(self, num_frames)`: Initializes a `Memory` object with a specified number of memory frames.
- `allocate_memory(self, process)`: Allocates memory for a given process.
- `deallocate_memory(self, pid)`: Deallocates memory for a process with the specified PID.
- `get_process(self, pid)`: Returns the process with the specified PID.

## Main Class Documentation

### Overview
The `Main` class is the main driver for the CPU scheduling simulation program. It loads processes, initializes CPU, memory, and scheduler, runs algorithms, displays metrics, and visualizes CPU activity.

### Attributes
- `directory`: Directory path containing text files of processes.

### Methods
- `__init__(self, directory)`: Initializes a `Main` object with a specified directory path.
- `load_processes(self, scheduler)`: Loads processes from text files and adds them to the scheduler.
- `run(self)`: Runs the main simulation, initializing components, loading processes, allocating memory, running selected algorithm, calculating metrics, and visualizing CPU activity.
