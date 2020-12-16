import re


class Rule:
    def __init__(self, name, range_1, range_2):
        self.name = name
        self.range_1 = range_1
        self.range_2 = range_2

    def in_range(self, target_number):
        return target_number in self.range_1 or target_number in self.range_2

rule_pattern = re.compile("([\\w ]+): (\\d+)-(\\d+) or (\\d+)-(\\d+)")
def parse_rule(line):
    match = rule_pattern.fullmatch(line.strip())
    if match:
        return Rule(match.group(1), range(int(match.group(2)), int(match.group(3)) + 1), range(int(match.group(4)), int(match.group(5)) + 1))
    else:
        raise ValueError(f"{line} did not match pattern {rule_pattern}")

def parse_ticket(line):
    return [int(num) for num in line.strip().split(",")]

def main():
    rules = []
    my_ticket = None
    other_tickets = []
    with open("input.txt") as file:
        for line in file:
            if line.isspace():
                break
            else:
                rules.append(parse_rule(line))

        file.readline() # "your ticket:"
        my_ticket = parse_ticket(file.readline()) # my ticket
        file.readline() # blank
        file.readline() # "nearby tickets:"

        for line in file:
            other_tickets.append(parse_ticket(line))

    error_sum = 0
    for ticket in other_tickets:
        for number in ticket:
            rule_pass = False
            for rule in rules:
                if rule.in_range(number):
                    rule_pass = True
                    break
            if not rule_pass:
                error_sum += number
    print(f"Error sum: {error_sum}")

if __name__ == "__main__":
    main()
