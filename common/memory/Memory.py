class Memory:
    def __init__(self, num_frames):
        self.page_table = {}
        self.physical_memory = [None] * num_frames

    def allocate_memory(self, process):
        available_frames = [i for i, frame in enumerate(self.physical_memory) if frame is None]
        if len(available_frames) == 0:
            return False

        frame_index = available_frames[0]
        self.page_table[process.pid] = frame_index
        self.physical_memory[frame_index] = process
        return True

    def deallocate_memory(self, pid):
        if pid not in self.page_table:
            return False

        frame_index = self.page_table[pid]
        self.physical_memory[frame_index] = None
        del self.page_table[pid]
        return True

    def get_process(self, pid):
        if pid not in self.page_table:
            return None

        frame_index = self.page_table[pid]
        return self.physical_memory[frame_index]
