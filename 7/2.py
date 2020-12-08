import re
import unittest

line_pattern = re.compile("(.+) bags contain (.+)")
contained_bag_pattern = re.compile("(\\d+) ([\\w ]+) bag[s]?")


def parse_line(line):
    parts = line_pattern.fullmatch(line.strip())
    if parts is None:
        raise ValueError(line)
    if parts == "no other bags.":
        return (outer_bag_color, [])

    outer_bag_color = parts.group(1)
    contained_bags_str = parts.group(2)
    contained_bags = []
    contained_bag_matches = contained_bag_pattern.findall(contained_bags_str)
    for contained_bag_match in contained_bag_matches: 
        contained_bags.append((int(contained_bag_match[0]), contained_bag_match[1]))

    return (outer_bag_color, contained_bags)

def invert_map(base):
    inverted = {}
    for key, values in base.items():
        for value in values:
            inverted.setdefault(value, []).append(key)
    return inverted

def sum_contains(color, bag_defs):
    sum = 0
    children = bag_defs[color]
    for child_count, child_color in children:
        sum += child_count * sum_contains(child_color, bag_defs)
        sum += child_count
    return sum

if __name__ == "__main__":
    bag_defs = {}
    with open("input.txt") as file:
        for line in file:
            bag_color, bag_contents = parse_line(line)
            bag_defs[bag_color] = bag_contents

    contains = {}
    for container, contents in bag_defs.items():
        contains[container] = []
        for count, contained_color in contents:
            contains[container].append(contained_color)

    gold_sum = sum_contains("shiny gold", bag_defs)
    print(f"1 shiny gold bag contains {gold_sum} child-bags")


class Tests(unittest.TestCase):
    def test_parseline(self):
        self.assertEqual(
            ("shiny gold", [(1, "dark olive"), (2, "vibrant plum")]),
            parse_line("shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags."))
        self.assertEqual(
            ("shiny gold", []),
            parse_line("shiny gold bags contain no other bags."))
    def test_invert(self):
        self.assertEqual(
            invert_map({"A": [1,2], "B": [2,3]}), 
            {1: ["A"], 2: ["A", "B"], 3: ["B"]})
