
class StateMachine:
    # instructions= cmd, value
    def __init__(self, instructions=None, base_state_machine=None, verbose=False):
        if instructions:
            self.name = "Base"
            self.instructions = instructions
            self.pc = 0
            self.acc = 0
            self.verbose = verbose
            self.seen_pc = set()
        elif base_state_machine: 
            self.name = f"Clone({base_state_machine.pc})"
            self.instructions = base_state_machine.instructions
            self.pc = base_state_machine.pc
            self.acc = base_state_machine.acc
            self.verbose = base_state_machine.verbose
            self.seen_pc = base_state_machine.seen_pc.copy()
        else:
            raise RuntimeError("Must initialize with instructions or base state machine")

    def current_instruction(self):
        return self.instructions[self.pc]

    def step(self):
        if self.pc >= len(self.instructions):
            raise IndexError("PC outside of instruction range")
        cmd, value = self.current_instruction()
        if cmd == "acc":
            self.acc += value
            self.pc += 1
        elif cmd == "jmp":
            self.pc += value
        elif cmd == "nop":
            self.pc += 1
        else:
            raise ValueError(f"Unrecognized command: {cmd}")

    def run_till_done(self, branch=False):
        while self.pc not in self.seen_pc:
            self.seen_pc.add(self.pc)
            if self.pc >= len(self.instructions):
                return True
            cmd, val = self.current_instruction()
            if branch and cmd in {"jmp", "nop"}:
                clone = StateMachine(base_state_machine=self)
                if cmd == "jmp":
                    clone.pc += 1
                elif cmd == "nop":
                    clone.pc += val
                if clone.run_till_done(branch=False):
                    print(f"Clone ACC: {clone.acc}")
                    return True
            self.say_state()
            self.step()
        if branch:
            print("Never found an out.")
        return False 

    def say_state(self):
        if self.verbose:
            print(f"Name: {self.name}\n  PC: {self.pc}\n  ACC: {self.acc}\n  CMD: {self.instructions[self.pc]}\n")

if __name__ == "__main__":
    instructions = []
    with open("input.txt") as file:
        for line in file:
            parts = line.split()
            instructions.append((parts[0], int(parts[1])))

    sm = StateMachine(instructions=instructions, verbose=True)
    final_acc = sm.run_till_done(branch=True)



