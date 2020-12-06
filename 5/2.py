import unittest


def decode(word, one_chr):
    sum = 0
    for idx, char in enumerate(word[::-1]):
        if char == one_chr:
            sum += 2**idx
    return sum

def get_pair(line):
    row = decode(line[:7], "B")
    col = decode(line[7:10], "R")
    return (row, col)

def to_id(seat_pair):
    return pair[0] * 8 + pair[1]

if __name__ == '__main__':
    seat_pairs = []
    seat_ids = []
    max_seat = 0
    with open("input.txt") as file:
        for line in file:
            pair = get_pair(line.strip())
            seat_pairs.append(pair)
            seat_id = to_id(pair)
            seat_ids.append(seat_id)
    
    seat_ids.sort()
    prior_seat = None
    for seat in seat_ids:
        if (seat - 2) == prior_seat:
            print(f"Empty Seat is: {seat - 1}")
        prior_seat = seat

class TestValidations(unittest.TestCase):
    def test_decode(self):
        self.assertEqual(44, decode("FBFBBFF", "B"))
        self.assertEqual(5, decode("RLR", "R"))
    def test_get_pair(self):
        self.assertEqual((44, 5), get_pair("FBFBBFFRLR"))
        self.assertEqual((31, 7), get_pair("FFBBBBBRRR"))
    def test_substring(self):
        self.assertEqual("FBFBBFF", "FBFBBFFRLR"[:7])
        self.assertEqual("FFBBFBF", "FBFBBFF"[::-1])
