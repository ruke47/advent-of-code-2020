import re


class Rule:
    def __init__(self, name, range_1, range_2):
        self.name = name
        self.range_1 = range_1
        self.range_2 = range_2

    def in_range(self, target_number):
        return target_number in self.range_1 or target_number in self.range_2

    def __str__(self):
        return f"Name: {self.name}, Ranges: {self.range_1, self.range_2}"

    def __repr__(self):
        return self.__str__()

class Ticket:
    def __init__(self, values):
        self.values = values

    def is_valid(self, rules):
        for number in self.values:
            if not any(rule.in_range(number) for rule in rules):
                return False
        return True
   
    def value(self, i):
        return self.values[i]

    def __str__(self):
        return self.values.__str__()

    def __repr__(self):
        return self.values.__repr__()


rule_pattern = re.compile("([\\w ]+): (\\d+)-(\\d+) or (\\d+)-(\\d+)")
def parse_rule(line):
    match = rule_pattern.fullmatch(line.strip())
    if match:
        return Rule(match.group(1), range(int(match.group(2)), int(match.group(3)) + 1), range(int(match.group(4)), int(match.group(5)) + 1))
    else:
        raise ValueError(f"{line} did not match pattern {rule_pattern}")

def parse_ticket(line):
    return Ticket([int(num) for num in line.strip().split(",")])

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
            ticket = parse_ticket(line)
            if ticket.is_valid(rules):
                other_tickets.append(ticket)
        
        other_tickets.append(my_ticket)

    valid_rules_by_value_index= {}
    for i in range(len(my_ticket.values)):
        all_values = [ticket.value(i) for ticket in other_tickets]
        matching_rules = [i for i, rule in enumerate(rules) if all(rule.in_range(value) for value in all_values)]
        print(f"[{i}] can be {matching_rules}")
        valid_rules_by_value_index[i] = matching_rules

    rule_to_value_mappings = {}
    while len(valid_rules_by_value_index) > 0:
        forced_rules = [(value_idx, valid_rules[0]) for value_idx, valid_rules in valid_rules_by_value_index.items() if len(valid_rules) == 1]
        if len(forced_rules) == 0:
            print(f"Ambiguity! Known Rules: {rule_to_value_mappings}\nRemaining: {valid_rules_by_value_index}")
            break
        print(f"Forced Rules: {forced_rules}")
        for value_idx, rule_idx in forced_rules:
            rule_to_value_mappings[rule_idx] = value_idx
            del valid_rules_by_value_index[value_idx]
            for rule_list in valid_rules_by_value_index.values():
                rule_list.remove(rule_idx)


    my_product = 1
    for rule_idx, rule in enumerate(rules):
        if rule.name.startswith("departure"):
            value_idx = rule_to_value_mappings[rule_idx]
            my_value = my_ticket.value(value_idx)
            print(f"{rule.name} = {my_value}")
            my_product *= my_value

    print(f"product: {my_product}")

if __name__ == "__main__":
    main()
