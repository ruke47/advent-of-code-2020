
adapters = []
with open("input.txt") as file:
    for line in file:
        adapters.append(int(line))

adapters.sort()

prior = 0
ones = 0
threes = 0
for adapter in adapters:
    if adapter == prior:
        print(f"Saw {adapter} twice in a row")
    elif adapter == prior + 1:
        ones += 1
    elif adapter == prior + 3:
        threes += 1
    elif adapter > prior + 3:
        print(f"Saw jump > 3 between {prior} and {adapter}.")
    prior = adapter
threes += 1
print(f"Ones: {ones} Threes: {threes} Mult: {ones * threes}")
