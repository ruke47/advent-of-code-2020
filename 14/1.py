import re
import unittest

mask_pattern = re.compile("mask = ([01X]+)")
write_pattern = re.compile("mem\\[(\d+)\\] = (\d+)")

def calculate_masks(mask_str):
    ones_mask = 0
    zeroes_mask = 2**36 - 1
    for i, char in enumerate(mask_str[::-1]):
        if char == "1":
            ones_mask += 2**i
        elif char == "0":
            zeroes_mask -= 2**i
    return (ones_mask, zeroes_mask)

def apply_masks(ones_mask, zeroes_mask, base_value):
    return base_value & zeroes_mask | ones_mask

def main():
    with open("input.txt") as file:
        ones_mask = None
        zeroes_mask = None
        memory = {}
        for line in file:
            mask_match = mask_pattern.fullmatch(line.strip())
            write_match = write_pattern.fullmatch(line.strip())
            if mask_match:
                ones_mask, zeroes_mask = calculate_masks(mask_match.group(1))
            elif write_match:
                address, value_str = write_match.group(1, 2)
                memory[int(address)] = apply_masks(ones_mask, zeroes_mask, int(value_str))
            else:
                raise ValueError("Neither pattern matched " + line)

        mem_sum = sum(memory.values())
        print(f"Sum of memory values is {mem_sum}")

class Tests(unittest.TestCase):
    def test_parse_masks(self):
        ones_mask, zeroes_mask = calculate_masks("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X")
        self.assertEqual(ones_mask, 64)
        self.assertEqual(zeroes_mask, 2**36 - 3)
        self.assertEqual(73, apply_masks(ones_mask, zeroes_mask, 11))
        self.assertEqual(101, apply_masks(ones_mask, zeroes_mask, 101))
        self.assertEqual(64, apply_masks(ones_mask, zeroes_mask, 0))

if __name__ == "__main__":
    main()
