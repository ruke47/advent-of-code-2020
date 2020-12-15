import re
import unittest

mask_pattern = re.compile("mask = ([01X]+)")
write_pattern = re.compile("mem\\[(\d+)\\] = (\d+)")

def calculate_masks(mask_str):
    ones_mask = 0
    floating_idx = []
    for i, char in enumerate(mask_str[::-1]):
        if char == "1":
            ones_mask += 2**i
        elif char == "X":
            floating_idx.append(i)
    return (ones_mask, floating_idx)

def get_all_addresses(base_address, floating_bits):
    if len(floating_bits) == 0:
        return [base_address]
    else:
        my_idx = floating_bits[-1]
        child_addresses = get_all_addresses(base_address, floating_bits[:-1])
        my_addresses = []
        for child_address in child_addresses:
            one_mask = 2**my_idx
            zero_mask = 2**36 - 1 - 2**my_idx
            my_addresses.append(child_address | one_mask)
            my_addresses.append(child_address & zero_mask)
        return my_addresses

def main():
    with open("input.txt") as file:
        ones_mask = None
        floating_bits = [] 
        memory = {}
        for line in file:
            mask_match = mask_pattern.fullmatch(line.strip())
            write_match = write_pattern.fullmatch(line.strip())
            if mask_match:
                ones_mask, floating_bits = calculate_masks(mask_match.group(1))
            elif write_match:
                base_address_str, value_str = write_match.group(1, 2)
                base_address = int(base_address_str) | ones_mask
                for address in get_all_addresses(base_address, floating_bits):
                    memory[int(address)] = int(value_str) 
            else:
                raise ValueError("Neither pattern matched " + line)

        mem_sum = sum(memory.values())
        print(f"Sum of memory values is {mem_sum}")

if __name__ == "__main__":
    main()
