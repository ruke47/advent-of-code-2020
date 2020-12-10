
class StateMachine:
    # instructions= cmd, value
    def __init__(self, instructions, verbose=False):
        self.instructions = instructions
        self.pc = 0
        self.acc = 0
        self.verbose = verbose

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

    def run_till_loop(self):
        seen_pc = set()
        while self.pc not in seen_pc:
            seen_pc.add(self.pc)
            self.step()
            self.say_state()
        return self.acc

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
    final_acc = sm.run_till_loop()
    print(f"Final acc: {final_acc}")



