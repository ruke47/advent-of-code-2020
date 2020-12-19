import regex

rule_pattern = regex.compile("(\\d+): (.*)")

class Pattern:
    def __init__(self, rule_map, rule_text):
        self.rule_map = rule_map
        self.rule_text = rule_text

    def detangle(self):
        if self.rule_text.startswith('"'):
            return self.rule_text[1]

        regex_str = ""
        for part in self.rule_text.split(" "):
            if part.isdecimal():
                regex_str += self.rule_map[part].detangle()
            else: 
                regex_str += part

        return "(?:" + regex_str + ")"

def main():
    rule_map = {}
    with open("input.txt") as file:
        for line in file:
            match = rule_pattern.fullmatch(line.strip())
            if match:
                rule_map[match.group(1)] = Pattern(rule_map, match.group(2))
            else:
                break

        rule_map["8"] = Pattern(rule_map, "42 +")
        rule_map["11"] = Pattern(rule_map, "42 (?R)? 31")

        gross_regex_str = rule_map["0"].detangle()
        print(f"Regex: {gross_regex_str}")
        rule_regex = regex.compile(gross_regex_str)

        matches = 0
        for line in file:
            if rule_regex.fullmatch(line.strip()):
                matches += 1

        print(f"{matches} matches")

if __name__ == "__main__":
    main()
