adapters = []
with open("input.txt") as file:
    for line in file:
        adapters.append(int(line))

adapters.sort()
adapters.append(adapters[-1] + 3)

prior = 0
diffs = {}
for val in adapters:
    diffs[val - prior] = diffs.get(val-prior, 0) + 1
    prior = val
print(diffs)
print(f"Mult: {diffs[1] * diffs[3]}")
