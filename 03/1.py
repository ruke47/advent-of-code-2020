
lines = []
with open("input.txt") as file:
    for line in file:
        lines.append(line.strip())

width = len(lines[0])
height = len(lines)
print(f"Width: {width} Height: {height}")

x = 0
y = 0
collisions = 0

while x < (height-1):
    x += 1
    y = (y + 3) % width
    print(f"({x}, {y})")
    if lines[x][y] == "#":
        collisions += 1

print(f"There were {collisions} collisions.")
