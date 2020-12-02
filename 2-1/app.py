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
            low = int(line_match.group(1))
            hi = int(line_match.group(2))
            letter = line_match.group(3)
            password = line_match.group(4)
            matches = re.findall(letter, password)
            if (len(matches) >= low and len(matches) <= hi):
                valid_count += 1
                if (verbose):
                    print(f"{password} matched {low} - {hi} {letter}")
            else:
                invalid_count += 1
                if (verbose):
                    print(f"{password} did not match {low} - {hi} {letter}") 

print(f"Valid: {valid_count}\nInvalid: {invalid_count}")


