import re
import unittest

expected_fields = {
    "byr": (lambda yr: validate_year(yr, 1920, 2002)), 
    "iyr": (lambda yr: validate_year(yr, 2010, 2020)),
    "eyr": (lambda yr: validate_year(yr, 2020, 2030)), 
    "hgt": (lambda hgt: validate_height(hgt)), 
    "hcl": (lambda hcl: bool(re.fullmatch("#[0-9a-f]{6}", hcl))), 
    "ecl": (lambda ecl: ecl in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}), 
    "pid": (lambda pid: bool(re.fullmatch("\\d{9}", pid))),
}
allowed_fields = {"cid"}


def validate_year(yr, min_year, max_year):
    if re.fullmatch("\\d{4}", yr) is None:
        return False
    int_yr = int(yr)
    return int_yr >= min_year and int_yr <= max_year

def validate_height(hgt):
    match = re.fullmatch("(\\d+)(cm|in)", hgt)
    if match is None:
        return False
    if match.group(2) == "cm":
        cms = int(match.group(1))
        return cms >= 150 and cms <= 193
    else:
        ins = int(match.group(1))
        return ins >= 59 and ins <= 76

if __name__ == '__main__':
    documents = []

    with open("input.txt") as file:
        cur_doc = {}
        for line in file:
            if line.isspace():
                documents.append(cur_doc)
                cur_doc = {}
            else:
                kvps = line.strip().split()
                for kvp in kvps:
                    parts = kvp.split(":", 1)
                    cur_doc[parts[0]] = parts[1]
        if cur_doc != {}:
            documents.append(cur_doc)

    valid_docs = 0
    invalid_docs = 0
    for doc in documents:
        if expected_fields.keys() <= doc.keys():
           for key, value in doc.items():
               valid = True
               if key in expected_fields.keys():
                   valid &= bool(expected_fields[key](value))
                   if not valid: 
                       print(f"Invalid: {key} - {{{value}}}")
                       break;
           if valid:
               valid_docs += 1
           else:
               invalid_docs += 1
        else:
            invalid_docs += 1

    print(f"Valid: {valid_docs} Invalid: {invalid_docs}")

class TestValidations(unittest.TestCase):
    def test_byr(self):
        self.assertEqual(expected_fields["byr"]("abc"), False)
        self.assertEqual(expected_fields["byr"]("1919"), False)
        self.assertEqual(expected_fields["byr"]("2003"), False)
        self.assertEqual(expected_fields["byr"]("1920"), True)
        self.assertEqual(expected_fields["byr"]("2002"), True)
        self.assertEqual(expected_fields["byr"]("1988"), True)
    def test_iyr(self):
        self.assertEqual(expected_fields["iyr"]("abc"), False)
        self.assertEqual(expected_fields["iyr"]("2009"), False)
        self.assertEqual(expected_fields["iyr"]("2021"), False)
        self.assertEqual(expected_fields["iyr"]("2010"), True)
        self.assertEqual(expected_fields["iyr"]("2020"), True)
    def test_hcl(self):
        self.assertEqual(expected_fields["hcl"]("red"), False)
        self.assertEqual(expected_fields["hcl"]("ff0000"), False)
        self.assertEqual(expected_fields["hcl"]("#aammzz"), False)
        self.assertEqual(expected_fields["hcl"]("#ff0000"), True)
        self.assertEqual(expected_fields["hcl"]("#946a88"), True)
