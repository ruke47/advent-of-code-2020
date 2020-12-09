
class Buffer:
    def __init__(self, size):
        self.capacity = size
        self.loaded = False
        self.array = []

    def add(self, val):
        while len(self.array) >= self.capacity:
            self.array.pop(0)
        self.array.append(val)
        self.loaded = len(self.array) == self.capacity

    def values(self):
        return self.array.copy()

def pair_sums(values, target):
    for i, val1 in enumerate(values):
        for j, val2 in enumerate(values):
            if i != j and val1 + val2 == target:
                return True
    return False

def main():
    with open("input.txt") as file:
        buf = Buffer(25)
        for line in file:
            val = int(line.strip())
            if buf.loaded:
                if not pair_sums(buf.values(), val):
                    print(f"Buffer does not contain a pair that sums to {val}")
                    return    
            buf.add(val)
    print(f"All values were sums of pairs in buffer?")

if __name__ == "__main__":
    main()


