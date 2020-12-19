import regex

rule_pattern = regex.compile("(\\d+): (.*)")

class Pattern:
    def __init__(self, rule_map, rule_text, name=None):
        self.rule_map = rule_map
        self.rule_text = rule_text
        self.name = name

    def detangle(self):
        # if the rule is quoted, just take the literal character
        if self.rule_text.startswith('"'):
            return self.rule_text[1]

        regex_str = ""
        for part in self.rule_text.split(" "):
            # if the part refers to another rule, append that rule's text 
            if part.isdecimal():
                regex_str += self.rule_map[part].detangle()
            # if the part is non-numeric, treat it as a string literal | or + or, uh, (?R)?
            # see https://www.regular-expressions.info/recurse.html
            else: 
                regex_str += part

        # surround yourself with a non-capturing group so letters don't smush together
        if self.name:
            return "(?P<" + self.name + ">" + regex_str + ")"
        else:
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

        # `8: 42 | 42 8` means "at least 1 of whatever 42 is
        rule_map["8"] = Pattern(rule_map, "42 +")
        # `11: 42 31 | 42 11 31` means "at least one 42, followed by the same number of 31's"
        rule_map["11"] = Pattern(rule_map, "42 (?&SR11)? 31", name="SR11")

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
