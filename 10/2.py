
adapters = []
with open("input.txt") as file:
    for line in file:
        adapters.append(int(line))

adapters.sort()

valid_ending_with = {0:1}

for val in adapters:
    cur_count = 0
    print(f"Testing {val}:")
    for delta in range(1, 4):
        new_count = valid_ending_with.get(val-delta, 0)
        cur_count += new_count
        print(f"\tValid ending with {val-delta} is {new_count}")
    valid_ending_with[val] = cur_count

biggest =  adapters[-1]
print(f"Valid ending with {biggest} is {valid_ending_with[biggest]}")
