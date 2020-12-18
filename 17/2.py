class Grid:
    def __init__(self, initial_grid=None):
        self.grid = {}
        if initial_grid:
            for z, row in enumerate(initial_grid):
                for w, val in enumerate(row):
                    if val == "#":
                        self.set(0, 0, z, w)

    def set(self, x, y, z, w):
        self.grid.setdefault(x, {}).setdefault(y, {}).setdefault(z, {})[w] = True

    def get(self, x, y, z, w):
        xgrid = self.grid.get(x)
        if xgrid:
            ygrid = xgrid.get(y)
            if ygrid:
                zgrid = ygrid.get(z)
                if zgrid:
                    return zgrid.get(w, False)
        return False

    def count_neighbors(self, x, y, z, w):
        count = 0
        for dx in range(-1,2):
            for dy in range(-1,2):
                for dz in range(-1,2):
                    for dw in range(-1,2):
                        if (dx, dy, dz, dw) != (0,0,0,0) and self.get(x+dx,y+dy,z+dz,w+dw):
                            count += 1
        return count

    def get_active_points(self):
        active_points = set()
        for x, xgrid in self.grid.items():
            for y, ygrid in xgrid.items():
                for z, zgrid in ygrid.items():
                    for w, value in zgrid.items():
                        if value:
                            active_points.add((x,y,z,w))
        return active_points               

    def get_points_to_check(self):
        points_to_check = set()
        for x, y, z, w in self.get_active_points():
            for dx in range(-1,2):
                for dy in range(-1,2):
                    for dz in range(-1,2):
                        for dw in range(-1,2):
                            points_to_check.add((x+dx, y+dy, z+dz, w+dw))
        return points_to_check

    def tick(self):
        new_grid = Grid()
        for x,y,z,w in self.get_points_to_check():
            neighbors = self.count_neighbors(x,y,z,w)
            if self.get(x,y,z,w) and neighbors in range(2,4):
                new_grid.set(x,y,z,w)
            elif neighbors == 3:
                new_grid.set(x,y,z,w)
        return new_grid
                
def main():
    tiles = []
    with open("input.txt") as file:
        for line in file:
            tiles.append(list(line.strip()))
    grid = Grid(tiles)
    for i in range(6):
        grid = grid.tick()

    print(f"Grid contains {len(grid.get_active_points())} tiles")

if __name__ == "__main__":
    main()
