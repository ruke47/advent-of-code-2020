
class StateMachine:
    # instructions= cmd, value
    def __init__(self, instructions, pc=0, acc=0, seen_pc=set(), verbose=False):
        self.instructions = instructions
        self.pc = pc
        self.acc = acc
        self.verbose = verbose
        self.seen_pc = seen_pc

    def step(self):
        if self.pc >= len(self.instructions):
            raise IndexError("PC outside of instruction range")
        cmd, value = self.instructions[self.pc]
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
            if branch and self.instructions[self.pc][0] == "jmp":
                clone = StateMachine(self.instructions, pc=self.pc + 1, acc=self.acc, seen_pc=self.seen_pc)
                if (clone.run_till_done()):
                    print(f"Clone ACC: {clone.acc}")
                    return True
            elif branch and self.instructions[self.pc][1] == "nop":
                clone = StateMachine(self.instructions, pc=self.pc + self.instructions[self.pc][1], acc=self.acc, seen_pc=self.seen_pc)
                if (clone.run_till_done()):
                    print(f"Clone ACC: {clone.acc}")
                    return True
            self.step()
            self.say_state()
        return False 

    def say_state(self):
        if self.verbose:
            print(f"PC: {self.pc}\nACC: {self.acc}\nCMD: {self.instructions[self.pc]}\n")

if __name__ == "__main__":
    instructions = []
    with open("input.txt") as file:
        for line in file:
            parts = line.split()
            instructions.append((parts[0], int(parts[1])))

    sm = StateMachine(instructions, True)
    final_acc = sm.run_till_done(branch=True)



