class Process:
    def __init__(self, pid, filename):
        self.pid = pid
        self.filename = filename
        self.arrival_time = 0
        self.code = {}
        self.read_process_data()

        self.executed_burst_time = 0
        self.initial_burst_time = 0
        self.burst_time = 0
        self.remaining_time = self.burst_time
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = None
        self.execution_status = False

    def read_process_data(self):
        with open(self.filename, 'r') as f:
            self.arrival_time = int(f.readline().strip())
            line_num = 1
            for line in f:
                parts = line.strip().split()
                instr = parts[0]
                args = parts[1].split(',') if len(parts) > 1 else []
                self.code[line_num] = [instr] + args
                line_num += 1
