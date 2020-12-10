
class Buffer:
    def __init__(self):
        self.array = []
        self.sum = 0

    def grow(self, val): 
       self.array.append(val)
       self.sum += val

    def shrink(self):
        self.sum -= self.array.pop(0)

    def values(self):
        return self.array.copy()

def main():
    target = 1398413738
    with open("input.txt") as file:
        buf = Buffer()
        for line in file:
            val = int(line.strip())
            buf.grow(val)
            while buf.sum > target:
                buf.shrink()
            if buf.sum == target:
                min_val = min(buf.values())
                max_val = max(buf.values())
                print(f"Buffer min: {min_val}, max: {max_val}, sum: {min_val + max_val}\nContents: {buf.values()}")
                return

if __name__ == "__main__":
    main()


