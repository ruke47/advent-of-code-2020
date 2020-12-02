import re

verbose = True
line_pattern = re.compile("(\\d+)-(\\d+) (\\w): (\\w+)")
valid_count = 0;
invalid_count = 0;
with open("input.txt") as file:
    for line in file:
        line_match = line_pattern.match(line)
        if line_match is None:
            print(f"{line} did not match the pattern")
        else:
            p1 = int(line_match.group(1)) - 1
            p2 = int(line_match.group(2)) - 1
            letter = line_match.group(3)
            password = line_match.group(4)
            matches = 0
            for position in (p1, p2):
                if position < len(password):
                    if password[position] == letter:
                        matches += 1

            if (matches == 1):
                valid_count += 1
                if (verbose):
                    print(f"{letter} was in position {p1} XOR {p2} of {password}")
            else:
                invalid_count += 1
                if (verbose):
                    print(f"got {matches} matches for letter {letter} in positions ({p1}, {p2}) of {password}") 

print(f"Valid: {valid_count}\nInvalid: {invalid_count}")


