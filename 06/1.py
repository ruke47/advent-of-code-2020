
if __name__ == '__main__':
    group_answers = []
    with open("input.txt") as file:
        group = {}
        for line in file:
            if line.isspace():
                group_answers.append(group)
                group = {}
            else:
                for q in line.strip():
                    group[q] = group.get(q, 0) + 1
        if group != {}:
            group_answers.append(group)

    sum_answers = 0
    for group in group_answers:
        sum_answers += len(group) 
    print(f"Unique answers: {sum_answers}")



