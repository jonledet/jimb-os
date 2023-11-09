class CPU:
    global_clock = 0

    def __init__(self):
        self.registers = [0] * 16
        self.alu = None
        self.program_counter = 0
        self.cache = None
        self.memory = {}

    def execute_instruction(self, instruction, simulate=False):
        opcode, *args = instruction
        if opcode == "ld":
            if not simulate:
                self.registers[int(args[0])] = self.memory.get(int(args[1]))
        elif opcode == "st":
            if not simulate:
                self.memory[int(args[1])] = self.registers[int(args[0])]
        elif opcode == "ldi":
            if not simulate:
                self.registers[int(args[0])] = int(args[1])
        elif opcode == "add":
            if not simulate:
                self.registers[int(args[0])] = self.registers[int(args[1])] + self.registers[int(args[2])]
        elif opcode == "addi":
            if not simulate:
                self.registers[int(args[0])] = self.registers[int(args[1])] + int(args[2])
        elif opcode == "sub":
            if not simulate:
                self.registers[int(args[0])] = self.registers[int(args[1])] - self.registers[int(args[2])]
        elif opcode == "and":
            if not simulate:
                self.registers[int(args[0])] = self.registers[int(args[1])] & self.registers[int(args[2])]
        elif opcode == "or":
            if not simulate:
                self.registers[int(args[0])] = self.registers[int(args[1])] | self.registers[int(args[2])]
        elif opcode == "xor":
            if not simulate:
                self.registers[int(args[0])] = self.registers[int(args[1])] ^ self.registers[int(args[2])]
        elif opcode == "sll":
            if not simulate:
                self.registers[int(args[0])] = self.registers[int(args[1])] << int(args[2])
        elif opcode == "srl":
            if not simulate:
                self.registers[int(args[0])] = self.registers[int(args[1])] >> int(args[2])
        else:
            raise ValueError(f"Unsupported opcode: {opcode}")
        return None

    def execute_process(self, process, time_quantum=None, check_preempt=None, simulate=False):
        self.program_counter = 1
        instructions_executed = 0

        while self.program_counter in process.code:
            if time_quantum is not None and instructions_executed >= time_quantum:
                break

            if check_preempt is not None and check_preempt(process):
                break

            instruction = process.code[self.program_counter]
            self.execute_instruction(instruction, simulate)
            self.program_counter += 1
            instructions_executed += 1

            if not simulate:
                CPU.global_clock += 1

        return instructions_executed

    def store_preempted_process(self, process):
        self.cache = process
