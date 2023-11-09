import os
import matplotlib.pyplot as plt
from common.core.CPU import CPU
from common.memory.Memory import Memory
from common.process.Process import Process
from common.scheduling.Scheduler import Scheduler


class Main:
    def __init__(self, directory):
        self.directory = directory

    def load_processes(self, scheduler):
        for filename in os.listdir(self.directory):
            if filename.endswith(".txt"):
                filepath = os.path.join(self.directory, filename)
                process = Process(filename.rstrip(".txt"), filepath)
                scheduler.add_process(process)

    def run(self):
        cpu = CPU()
        memory = Memory(num_frames=10)
        scheduler = Scheduler(memory)
        self.load_processes(scheduler)

        for process in scheduler.process_list:
            memory.allocate_memory(process)

        scheduler.compute_burst_times(cpu)
        for process in scheduler.process_list:
            process.initial_burst_time = process.burst_time

        print("Please select a scheduling algorithm:")
        print("1. First Come First Serve (FCFS)")
        print("2. Round Robin (RR)")
        print("3. Shortest Process Next (SPN)")
        print("4. Shortest Remaining Time (SRT)")
        choice = int(input("Enter the number corresponding to your choice: "))

        time_quantum = 0
        if choice == 1:
            scheduler.run_FCFS(cpu)
            algorithm_name = 'FCFS'
        elif choice == 2:
            time_quantum = int(input("Enter the time quantum for Round Robin scheduling: "))
            scheduler.run_RR(cpu, time_quantum)
            algorithm_name = 'RR'
        elif choice == 3:
            scheduler.run_SPN(cpu)
            algorithm_name = 'SPN'
        elif choice == 4:
            scheduler.run_SRT(cpu)
            algorithm_name = 'SRT'
        else:
            print("Invalid choice. Exiting.")
            return

        performance_metrics = scheduler.calculate_performance_metrics()

        if algorithm_name == 'RR':
            scheduler.visualize_cpu_activity(algorithm_name, time_quantum)
            scheduler.display_performance_metrics_table(performance_metrics, algorithm_name, time_quantum)
        else:
            scheduler.visualize_cpu_activity(algorithm_name)
            scheduler.display_performance_metrics_table(performance_metrics, algorithm_name)

        plt.show()


if __name__ == "__main__":
    directory = input("Enter the directory path containing the .txt files: ")
    main = Main(directory)
    main.run()
