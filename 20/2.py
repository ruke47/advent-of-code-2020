import regex
import unittest

title_pattern = regex.compile("Tile (\\d+):")

def arr_to_int(line):
    width = len(line)
    val = 0
    val_i = 0
    for i, char in enumerate(line):
        val <<= 1
        if char == "#":
            val += 1
            val_i += 1<<i
    return val, val_i
        
class Tile:
    def __init__(self, name, lines):
        self.name = name
        match = title_pattern.fullmatch(name)
        if match:
            self.id = int(match.group(1))
        self.lines = lines
        self.size = len(lines)
        self.top, self.top_i  = arr_to_int(lines[0])
        self.right, self.right_i = arr_to_int([line[-1] for line in lines])
        self.bottom, self.bottom_i = arr_to_int(lines[-1])
        self.left, self.left_i = arr_to_int([line[0] for line in lines])
        self.rotations = 0
        self.vflip = False
        self.hflip = False
        if len(self.all_sides()) < 8:
            raise ValueError("Gross! Two sides look kinda the same! " + lines)

    def flip_h(self):
        self.top, self.bottom, = self.bottom, self.top
        self.top_i, self.bottom_i = self.bottom_i, self.top_i
        self.left, self.left_i = self.left_i, self.left
        self.right, self.right_i = self.right_i, self.right
        self.hflip = not self.hflip

    def flip_v(self):
        self.top, self.top_i, = self.top_i, self.top
        self.bottom, self.bottom_i = self.bottom_i, self.bottom
        self.left, self.right = self.right, self.left
        self.left_i, self.right_i = self.right_i, self.left_i
        self.vflip = not self.vflip

    def rotate(self):
       self.top, self.right, self.bottom, self.left, self.top_i, self.right_i, self.bottom_i, self.left_i = self.left_i, self.top, self.right_i, self.bottom, self.left, self.top_i, self.right, self.bottom_i
       self.rotations += 1
       self.rotations %= 4

    def all_sides(self, include_inverse=True):
        if include_inverse:
            return {self.top, self.bottom, self.left, self.right, self.top_i, self.bottom_i, self.left_i, self.right_i}
        else:
            return {self.top, self.bottom, self.left, self.right}
    
    def orient(self, top=None, left=None):
        if left: 
            while left not in {self.left, self.left_i}:
                self.rotate()
            if self.left != left:
                self.flip_h()
        elif top:
            while top not in {self.top, self.top_i}:
                self.rotate()
            if self.top != top:
                self.flip_v()
        else:
            raise ValueError("Specify left or top!")

def main():
    tiles = []
    with open("input.txt") as file:
        while True:
            name = file.readline().strip()
            lines = []
            for line in file:
                if line.isspace():
                    break
                else:
                    lines.append(line.strip())
            if lines:
                tiles.append(Tile(name, lines))
            else:
                break

    all_edges = {}
    for tile in tiles:
        for side in tile.all_sides():
            all_edges.setdefault(side, []).append(tile)

    only_one = [name for name, tiles in all_edges.items() if len(tiles) == 1]
    more_than_two = [name for name, count in all_edges.items() if len(tiles) > 2]
    only_one.sort()
    more_than_two.sort()
    print(f"only_one_instance: {len(only_one)}\nmore_than_two: {len(more_than_two)}")
    
    edge_numbers = set(only_one)
    corner_tiles = [tile for tile in tiles if len(edge_numbers & tile.all_sides()) == 4]
    edge_tiles = [tile for tile in tiles if len(edge_numbers & tile.all_sides()) == 2] 
    print(f"Found {len(corner_tiles)} corner tiles and {len(edge_tiles)} edge tiles")
    
    #pick a corner tile, and rotate it until it's unmatched sides are right and top. define this h/v flip as "correct"
    solved = [[None] * 12 for i in range(12)]
    solved[0][0] = corner_tiles.pop()
    while not {solved[0][0].left, solved[0][0].top} <= edge_numbers:
        solved[0][0].rotate()
    # find an edge tile whose left edge matches the prior solved tile's right edge
    for i in range(1,11):
        prior = solved[0][i-1]
        candidates = [tile for tile in edge_tiles if prior.right in tile.all_sides()]
        top_matches = []
        for tile in candidates:
            tile.orient(left=prior.right)
            if tile.top in edge_numbers:
                top_matches.append(tile)

        if len(top_matches) > 1:
            raise Exception(f"Found {len(top_matches)} tiles that might go at: ({i}, 0)")        
        if not top_matches:
            raise Exception(f"Couldn't find a candidate to got at: ({i}, 0)")

        # rotate and flip this tile until it's left edge looks like the right edge of the solved tile to the right
        solved[0][i] = top_matches[0]
        edge_tiles.remove(top_matches[0])

    # find the top-right corner
    top_right = [tile for tile in corner_tiles if solved[0][10].right in tile.all_sides()][0]
    top_right.orient(left=solved[0][10].right)
    solved[0][11] = top_right
    corner_tiles.remove(top_right)

    for j in (0, 11):
        for i in range(1,11):
            prior = solved[i-1][j]
            candidates = [tile for tile in edge_tiles if prior.bottom in tile.all_sides()]
            side_matches = []
            for tile in candidates:
                tile.orient(top=prior.bottom)
                side = tile.left if j == 0 else tile.right
                if side in edge_numbers:
                    side_matches.append(tile)

            if len(side_matches) > 1:
                raise Exception(f"Found {len(top_matches)} tiles that might go at {i, j}")
            if not side_matches:
                raise Exception(f"Couldn't find a candidate to go at {i, j}")

            solved[i][j] = side_matches[0]
            edge_tiles.remove(side_matches[0])

        bottom_corner = [tile for tile in corner_tiles if solved[10][j].bottom in tile.all_sides()][0]
        bottom_corner.orient(top=solved[10][j].bottom)
        solved[11][j] = bottom_corner
        corner_tiles.remove(bottom_corner)

        middle_tiles = set([tile for tile in tiles if tile.all_sides().isdisjoint(edge_numbers)])
        for i in range(1,11):
            for j in range(1,11):
                top_neighbor = solved[i-1][j]
                left_neighbor  = solved[i][j-1]
                candidates = [tile for tile in middle_tiles if {top_neighbor.bottom, left_neighbor.right} <= tile.all_sides()]
                filtered_candidates = []
                for tile in candidates:
                    tile.orient(top=top_neighbor.bottom)
                    if tile.left == left_neighbor.right:
                        filtered_candidates.append(tile)

                if len(filtered_candidates) > 1:
                    raise Exception(f"Found {len(filtered_candidates)} that might go at {i, j}")
                elif not filtered_candidates:
                    raise Exception(f"Couldn't find a candidate to go at {i,j}")

                solved[i][j] = filtered_candidates[0]
                middle_tiles.remove(filtered_candidates[0])



class Test(unittest.TestCase):
    def test_parse_arr(self):
        self.assertEqual(arr_to_int(list("..#.#.##")), (0b00101011, 0b11010100))

    def ref_tile(self):
        return Tile("test", [
            "#.#.#####.", 
            ".#..######",
            "..#.......",
            "######....",
            "####.#..#.",
            ".#...#.##.",
            "#.#####.##",
            "..#.###...",
            "..#.......",
            "..#.###..."])
    def test_tile(self):
        tile = self.ref_tile()
        self.assertEqual((tile.top, tile.right, tile.bottom, tile.left), (0b1010111110, 0b0100001000, 0b0010111000, 0b1001101000))
        self.assertEqual((tile.top_i, tile.right_i, tile.bottom_i, tile.left_i), (0b0111110101, 0b0001000010, 0b0001110100, 0b0001011001))

    def test_rotate(self):
        tile = self.ref_tile()
        tile.rotate()
        self.assertEqual((tile.top, tile.right, tile.bottom, tile.left), (0b0001011001, 0b1010111110, 0b0001000010, 0b0010111000))
        self.assertEqual((tile.top_i, tile.right_i, tile.bottom_i, tile.left_i), (0b1001101000, 0b0111110101, 0b0100001000, 0b0001110100))

    def test_flip_v(self):
        tile = self.ref_tile()
        tile.flip_v()
        self.assertEqual((tile.top, tile.right, tile.bottom, tile.left), (0b0111110101, 0b1001101000, 0b0001110100, 0b0100001000))
        self.assertEqual((tile.top_i, tile.right_i, tile.bottom_i, tile.left_i), (0b1010111110, 0b0001011001, 0b0010111000, 0b0001000010))

    def test_filp_h(self):
        tile = self.ref_tile()
        tile.flip_h()
        self.assertEqual((tile.top, tile.right, tile.bottom, tile.left), (0b0010111000, 0b0001000010, 0b1010111110, 0b0001011001))
        self.assertEqual((tile.top_i, tile.right_i, tile.bottom_i, tile.left_i), (0b0001110100, 0b0100001000, 0b0111110101, 0b1001101000))

if __name__ == "__main__":
    main()
