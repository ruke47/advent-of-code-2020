
lines = []
with open("input.txt") as file:
    for line in file:
        lines.append(line.strip())

width = len(lines[0])
height = len(lines)
print(f"Width: {width} Height: {height}")

# x,y
slopes = ((1,1), (1,3), (1,5), (1,7), (2,1))
collision_mult = 1

for dx, dy in slopes:
    x = 0
    y = 0
    collisions = 0

    while x < (height-dx):
        x += dx
        y = (y + dy) % width
        if lines[x][y] == "#":
            collisions += 1

    print(f"({dx}, {dy}): {collisions} collisions")
    collision_mult *= collisions

print(f"{collision_mult} multiplied collisions")
