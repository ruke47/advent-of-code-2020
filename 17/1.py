import unittest

class Grid:
    def __init__(self, initial_grid=None):
        self.grid = {}
        if initial_grid:
            for y, row in enumerate(initial_grid):
                for z, val in enumerate(row):
                    if val == "#":
                        self.set(0, y, z)

    def set(self, x, y, z):
        self.grid.setdefault(x, {}).setdefault(y, {})[z] = True

    def unset(self, x, y, z):
        xgrid = self.grid.get(x)
        if xgrid:
            ygrid = xgrid.get(y)
            if ygrid and z in ygrid:
                del ygrid[z]

    def get(self, x, y, z):
        xgrid = self.grid.get(x)
        if xgrid:
            ygrid = xgrid.get(y)
            if ygrid:
                return ygrid.get(z, False)
        return False

    def count_neighbors(self, x, y, z):
        count = 0
        for dx in range(-1,2):
            for dy in range(-1,2):
                for dz in range(-1,2):
                    if (dx, dy, dz) != (0,0,0) and self.get(x+dx,y+dy,z+dz):
                        count += 1
        return count

    def get_active_points(self):
        active_points = set()
        for x, xgrid in self.grid.items():
            for y, ygrid in xgrid.items():
                for z, value in ygrid.items():
                    if value:
                        active_points.add((x,y,z))
        return active_points               

    def get_points_to_check(self):
        points_to_check = set()
        for x, y, z in self.get_active_points():
            for dx in range(-1,2):
                for dy in range(-1,2):
                    for dz in range(-1,2):
                        points_to_check.add((x+dx, y+dy, z+dz))
        return points_to_check

    def tick(self):
        new_grid = Grid()
        for x,y,z in self.get_points_to_check():
            neighbors = self.count_neighbors(x,y,z)
            if self.get(x,y,z) and neighbors in range(2,4):
                new_grid.set(x,y,z)
            elif neighbors == 3:
                new_grid.set(x,y,z)
        return new_grid

                
"""
    def set(self, *args):
        cur_grid = self.grid
        for point in args[:-1]:
            cur_grid = cur_grid.setdefault(point, {})
        cur_grid[args[-1]] = True

         

    def unset(self, *args):
        cur_grid = self.grid
        for point in args[:-1]:
            cur_grid = cur_grid.get(point)
            if cur_grid is None:
                return
        cur_grid[args[-1]] = False

    def r_unset(self, base_grid, point, *args):
        if base_grid is None:
            return
        if not args and point in base_grid:
            del base_grid[point]
        else
            self.r_unset(base_grid[point], args)
            


    def get(self, *args):
        cur_grid = self.grid
        for point in args:
            cur_grid = cur_grid.get(point)
            if cur_grid is None:
                return False
        return cur_grid

    def count_neighbors(self, *args):
        neighbors = 0
        x,y,z = args
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                for dz in range(-1, 2):
                    if (dx, dy, dz) != (0,0,0) and self.get(x+dx, y+dy, z+dz):
                        neighbors += 1
        return neighbors
"""

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

class TestGrid(unittest.TestCase):
    def test_set(self):
        grid = Grid([[]], 3)
        self.assertEqual({}, grid.grid)
        grid.set(1,2,3)
        self.assertEqual({1: {2: {3: True} } }, grid.grid)
        grid.set(1,2,4)
        self.assertEqual({1: {2: {3: True, 4: True}}}, grid.grid)
        grid.set(2, 2, 3)
        self.assertEqual({1: {2: {3: True, 4: True}}, 2: {2: {3: True}}}, grid.grid)
        grid.unset(4,5,6)
        self.assertEqual({1: {2: {3: True, 4: True}}, 2: {2: {3: True}}}, grid.grid)
        grid.unset(1,2,3)
        self.assertEqual({1: {2: {3: False, 4: True}}, 2: {2: {3: True}}}, grid.grid)
    
    def test_count(self):
        grid = Grid([
            list(".#."),
            list("..#"),
            list("###")
        ], 3)
        self.assertEqual({0: {0: {1: True}, 1: {2: True}, 2: {0: True, 1: True, 2: True}}}, grid.grid)
        self.assertEqual(grid.count_neighbors(0,0,1), 1)
        self.assertEqual(grid.count_neighbors(0,1,1), 5)
        grid.set(-1,1,1)
        grid.set(1,1,1)
        self.assertEqual(grid.count_neighbors(0,1,1), 7)
