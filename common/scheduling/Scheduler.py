import heapq
from collections import deque
from matplotlib import pyplot as plt
import pandas as pd


class Scheduler:
    def __init__(self, memory):
        self.memory = memory
        self.ready_queue = deque()
        self.process_list = []
        self.cpu_activity_log = pd.DataFrame(columns=['pid', 'start_time', 'end_time'])

    def add_process(self, process):
        self.process_list.append(process)

    def compute_burst_times(self, cpu):
        for process in self.process_list:
            cpu.global_clock = 0
            process.burst_time = cpu.execute_process(process, simulate=True)

    def run_FCFS(self, cpu):
        self.cpu_activity = []
        self.ready_queue = deque(sorted(self.process_list, key=lambda p: p.arrival_time))
        while self.ready_queue:
            process = self.ready_queue.popleft()
            if cpu.global_clock < process.arrival_time:
                cpu.global_clock = process.arrival_time

            process.waiting_time = cpu.global_clock - process.arrival_time
            if process.response_time is None:
                process.response_time = process.waiting_time

            start_time = cpu.global_clock
            instructions_executed = cpu.execute_process(process)
            end_time = cpu.global_clock + instructions_executed
            self.memory.deallocate_memory(process.pid)

            process.turnaround_time = end_time - process.arrival_time
            self.record_cpu_activity(process.pid, start_time, end_time)

            cpu.global_clock = end_time

    def run_RR(self, cpu, time_quantum):
        self.cpu_activity = []
        self.ready_queue = deque(sorted(self.process_list, key=lambda p: p.arrival_time))
        executed_processes = []

        while self.ready_queue or executed_processes:
            while self.ready_queue and self.ready_queue[0].arrival_time <= cpu.global_clock:
                process = self.ready_queue.popleft()
                executed_processes.append(process)

            if not executed_processes:
                cpu.global_clock = self.ready_queue[0].arrival_time
                continue

            process = executed_processes.pop(0)
            start_time = cpu.global_clock
            time_to_execute = min(process.burst_time, time_quantum)
            instructions_executed = cpu.execute_process(process, time_quantum=time_to_execute)
            cpu.global_clock += instructions_executed
            end_time = cpu.global_clock
            self.memory.deallocate_memory(process.pid)

            if process.response_time is None:
                process.response_time = start_time - process.arrival_time

            process.waiting_time += start_time - process.arrival_time - process.executed_burst_time
            process.executed_burst_time += instructions_executed

            if instructions_executed < process.burst_time:
                process.burst_time -= instructions_executed
                self.ready_queue.append(process)
            else:
                process.turnaround_time = end_time - process.arrival_time

            self.record_cpu_activity(process.pid, start_time, end_time)

    def run_SPN(self, cpu):
        self.cpu_activity = []
        self.ready_queue = deque(sorted(self.process_list, key=lambda p: p.arrival_time))
        executed_processes = []

        while self.ready_queue or executed_processes:
            while self.ready_queue and self.ready_queue[0].arrival_time <= cpu.global_clock:
                process = self.ready_queue.popleft()
                executed_processes.append(process)

            if not executed_processes:
                cpu.global_clock = self.ready_queue[0].arrival_time
                continue

            executed_processes = sorted(executed_processes, key=lambda p: p.burst_time)
            process = executed_processes.pop(0)

            process.waiting_time = cpu.global_clock - process.arrival_time
            if process.response_time is None:
                process.response_time = process.waiting_time

            start_time = cpu.global_clock
            instructions_executed = cpu.execute_process(process)
            end_time = cpu.global_clock + instructions_executed
            self.memory.deallocate_memory(process.pid)

            process.turnaround_time = end_time - process.arrival_time
            self.record_cpu_activity(process.pid, start_time, end_time)

            cpu.global_clock = end_time

    def run_SRT(self, cpu):
        self.cpu_activity = []
        self.ready_queue = deque(sorted(self.process_list, key=lambda p: p.arrival_time))
        executed_processes = []

        while self.ready_queue or executed_processes:
            while self.ready_queue and self.ready_queue[0].arrival_time <= cpu.global_clock:
                process = self.ready_queue.popleft()
                executed_processes.append(process)

            if not executed_processes:
                cpu.global_clock = self.ready_queue[0].arrival_time
                continue

            executed_processes = sorted(executed_processes, key=lambda p: p.burst_time)
            process = executed_processes.pop(0)

            process.waiting_time = cpu.global_clock - process.arrival_time
            if process.response_time is None:
                process.response_time = process.waiting_time

            def check_preempt(process_list, current_process, global_clock):
                for proc in process_list:
                    if proc.arrival_time <= global_clock and proc.burst_time < current_process.burst_time:
                        return True
                return False

            preemption = False
            start_time = cpu.global_clock
            instructions_executed = 0
            while not preemption and process.burst_time > 0:
                instructions_executed += cpu.execute_process(process, time_quantum=1)
                process.burst_time -= 1
                cpu.global_clock += 1
                end_time = cpu.global_clock
                preemption = check_preempt(self.ready_queue, process, cpu.global_clock)
                if preemption:
                    executed_processes.append(process)
                    self.ready_queue.append(process)

            if not preemption:
                process.turnaround_time = cpu.global_clock - process.arrival_time

            self.memory.deallocate_memory(process.pid)
            self.record_cpu_activity(process.pid, start_time, end_time)

    def record_cpu_activity(self, pid, start_time, end_time):
        existing_activity = self.cpu_activity_log[
            (self.cpu_activity_log['pid'] == pid) & (self.cpu_activity_log['end_time'] == start_time)]

        if not existing_activity.empty:
            index = existing_activity.index[0]
            self.cpu_activity_log.at[index, 'end_time'] = end_time
        else:
            self.cpu_activity_log.loc[len(self.cpu_activity_log)] = [pid, start_time, end_time]

    def calculate_performance_metrics(self):
        performance_metrics = []

        for process in self.process_list:
            arrival_time = process.arrival_time
            burst_time = process.initial_burst_time
            response_time = process.response_time
            turnaround_time = process.turnaround_time
            normalized_turnaround_time = turnaround_time / process.initial_burst_time

            performance_metrics.append({
                'pid': process.pid,
                'arrival_time': arrival_time,
                'burst_time': burst_time,
                'response_time': response_time,
                'turnaround_time': turnaround_time,
                'normalized_turnaround_time': normalized_turnaround_time
            })

        return performance_metrics

    def display_performance_metrics_table(self, performance_metrics, algorithm_name, time_quantum=None):
        column_labels = ['Process', 'Arrival Time', 'Burst Time', 'Response Time', 'Turnaround Time',
                         'Normalized Turnaround Time']
        table_data = [
            [metric['pid'], metric['arrival_time'], metric['burst_time'], metric['response_time'],
             metric['turnaround_time'], metric['normalized_turnaround_time']]
            for metric in performance_metrics]

        fig, ax = plt.subplots()
        ax.axis('tight')
        ax.axis('off')

        fontsize = 14
        table = ax.table(cellText=table_data, colLabels=column_labels, cellLoc='center', loc='center',
                         fontsize=fontsize)
        table.auto_set_font_size(False)
        table.set_fontsize(fontsize)
        table.scale(1.2, 1.2)

        title = f'Performance Metrics - {algorithm_name}'
        if time_quantum is not None:
            title += f' - Time Quantum: {time_quantum}'
        ax.set_title(title, fontsize=16)

        plt.show(block=False)

    def visualize_cpu_activity(self, algorithm_name, time_quantum=None):
        fig, ax = plt.subplots()
        y_labels = []
        y_ticks = []

        process_rows = {}
        for i, row in self.cpu_activity_log.iterrows():
            pid, start_time, end_time = row['pid'], row['start_time'], row['end_time']
            if pid not in process_rows:
                process_rows[pid] = []
            process_rows[pid].append((start_time, end_time - start_time))

        for i, pid in enumerate(sorted(process_rows.keys())):
            y_labels.append(f'P{pid}')
            y_ticks.append(i)
            ax.broken_barh(process_rows[pid], (i - 0.4, 0.8), facecolors='blue')

        ax.set_yticks(y_ticks)
        ax.set_yticklabels(y_labels, fontsize=16)
        ax.set_xticks(range(0, int(self.cpu_activity_log['end_time'].max()) + 1, 1))
        ax.set_xticklabels(range(0, int(self.cpu_activity_log['end_time'].max()) + 1, 1), fontsize=16)
        ax.set_xlabel('Time', fontsize=16)
        ax.set_ylabel('Processes', fontsize=16)
        title = f'CPU Activity (Gantt Chart) - {algorithm_name}'
        if time_quantum is not None:
            title += f' - Time Quantum: {time_quantum}'
        ax.set_title(title, fontsize=18)
        ax.grid(True)

        plt.show(block=False)

