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

expected_fields = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
allowed_fields = {"cid"}

valid_docs = 0
invalid_docs = 0
for doc in documents:
    if expected_fields <= doc.keys():
        valid_docs += 1
    else:
        invalid_docs += 1

print(f"Valid: {valid_docs} Invalid: {invalid_docs}")

