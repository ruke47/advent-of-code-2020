import unittest
from itertools import repeat

class Board:
    def __init__(self, board):
        self.board = board
        self.height = len(board)
        self.width = len(board[0])

    def count_neighbors(self, x, y) :
        count = 0
        for dx in range(-1, 2):
            tx = x + dx
            if tx < 0 or tx >= self.height:
                continue
            for dy in range(-1, 2):
                ty = y + dy
                if dx == 0 and dy == 0:
                    continue
                if ty < 0 or ty >= self.width:
                    continue
                if self.board[tx][ty] == "#":
                    count += 1
        return count

    def tick(self):
        new_board = []   
        for x, row  in enumerate(self.board):
            new_board.append([None] * self.width)
            for y, val in enumerate(row):
                if val == ".":
                    new_board[x][y] = "."
                else:
                    neighbors = self.count_neighbors(x, y)
                    if val == "L" and neighbors == 0:
                        new_board[x][y] = "#"
                    elif val == "#" and neighbors > 3:
                        new_board[x][y] = "L"
                    else:
                        new_board[x][y] = val
        return Board(new_board)

    def __eq__(self, other):
        if isinstance(other, Board):
            return self.board == other.board
        else:
            return False

    def __str__(self):
        return self.board.__str__()
    def __repr__(self):
        return self.board.__repr__()

def main():
    tiles = []
    with open("input.txt") as file:
        for line in file:
            tiles.append(list(line.strip()))
    
    cur_board = Board(tiles)
    prior_board = None
    tick_count = 0
    while cur_board != prior_board and tick_count < 10000:
        tick_count += 1
        prior_board = cur_board
        cur_board = cur_board.tick()

    seated_count = 0
    for row in cur_board.board:
        for val in row:
            if val == "#":
                seated_count += 1
    print(f"{seated_count} seated after {tick_count} ticks")


class Test(unittest.TestCase):
    def test_count(self):
        board = Board([
            list("L.#"),
            list("##."),
            list("L#L"),
            list(".L.")
        ])
        self.assertEqual(board.count_neighbors(0,0), 2)
        self.assertEqual(board.count_neighbors(0,2), 1)
        self.assertEqual(board.count_neighbors(3,0), 1)
        self.assertEqual(board.count_neighbors(3,2), 1)
        self.assertEqual(board.count_neighbors(1,1), 3)

    def test_tick(self):
        board0 = Board([
            list("LLL"),
            list("LLL"),
            list("LLL")
        ])

        expected1 = Board([
            list("###"),
            list("###"),
            list("###"),
        ])

        expected2 = Board([
            list("#L#"),
            list("LLL"),
            list("#L#"),
        ])

        self.assertEqual(board0, board0)
        board1 = board0.tick()
        self.assertEqual(board1, expected1)
        board2 = board1.tick()
        self.assertEqual(board2, expected2)
        board3 = board2.tick()
        # there should be no advancement after reaching expected2
        self.assertEqual(board3, board2)

if __name__ == "__main__":
    main()
