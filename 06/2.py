
if __name__ == '__main__':
    group_answers = []
    with open("input.txt") as file:
        group = {}
        group_size = 0
        for line in file:
            if line.isspace():
                group_answers.append((group, group_size))
                group = {}
                group_size = 0
            else:
                group_size += 1
                for q in line.strip():
                    group[q] = group.get(q, 0) + 1
        if group != {}:
            group_answers.append((group, group_size))

    sum_answers = 0
    for group, group_size in group_answers:
        for count in group.values():
            if count == group_size:
                sum_answers += 1
    print(f"Unique answers: {sum_answers}")



