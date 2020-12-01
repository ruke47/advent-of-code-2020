ints = []
with open("input.txt") as file:
    for line in file:
        if line:
            ints.append(int(line))

for i_1, v_1 in enumerate(ints):
    for i_2, v_2 in enumerate(ints[(i_1 + 1):]):
        if v_1 + v_2 == 2020:
            print(f"[{i_1}, {i_2}]: {v_1} * {v_2} = {v_1 * v_2}")
