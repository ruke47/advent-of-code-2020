from unittest import TestCase

def tokenize(text_iter):
    cur_text = ""
    tokens = []
    for char in text_iter:
        if char.isspace():
            pass
        elif char.isdecimal():
            cur_text += char
        else:
            if cur_text:
                tokens.append(int(cur_text))
                cur_text = ""

            if char in {"+", "*"}:
                tokens.append(char)
            elif char == "(":
                tokens.append(tokenize(text_iter))
            elif char == ")":
                return tokens
    if cur_text:
        tokens.append(int(cur_text))
    return tokens
        

def calc(tokens):
    return calc_products(calc_sums(tokens))

def calc_sums(tokens):
    output_tokens = []
    prior_token = get_val(tokens[0])
    token_iter = iter(tokens[1:])
    for token in token_iter:
        operator = token
        next_val = get_val(next(token_iter))
        if operator == "+":
            prior_token = prior_token + next_val
        else:
            output_tokens.append(prior_token)
            output_tokens.append(operator)
            prior_token = next_val
    output_tokens.append(prior_token)
    return output_tokens

def calc_products(tokens):
    product = get_val(tokens[0])
    token_iter = iter(tokens[1:])
    for token in token_iter:
        operator = token
        next_val = get_val(next(token_iter))
        if operator == "*":
            product *= next_val
        else:
            raise ValueError(f"Unexpected Operator: {operator}")
    return product

def get_val(item):
    if isinstance(item, list):
        return calc(item)
    elif isinstance(item, int):
        return item
    else:
        raise ValueError(f"I dont know how to get the value of: {item}")

def main():
    sum = 0
    with open("input.txt") as file:
        for line in file:
            try:
                sum += calc(tokenize(iter(line)))
            except Exception as e:
                print(f"Failed on: {line}")
                raise e
    print(f"Sum = {sum}")

if __name__ == "__main__":
    main()

class CalcTest(TestCase):
    def test_token(self):
        self.assertEqual([1, "+", 23, "*", 45], tokenize(iter("1 + 23 * 45")))
        self.assertEqual([1, "+", [23, "*", 45]], tokenize(iter("1 + (23 * 45)")))
        self.assertEqual([[1, "+", 23], "*", 45], tokenize(iter("(1 + 23) * 45")))
        self.assertEqual([[[1, "+", 23], "*", 45], "+", 6], tokenize(iter("((1 + 23) * 45) + 6")))
        self.assertEqual([1, "+", [23, "*", [45, "+", 6]], "*", [7, "+", 89]], tokenize(iter("1 + (23 * (45 + 6)) * (7 + 89)")))

    def test_simple_sum(self):
        self.assertEqual(calc(tokenize(iter("1 + 2 * 3 + 4"))), 21)
        self.assertEqual(calc(tokenize(iter("1 + 23 * 45"))), 1080)
        self.assertEqual(calc(tokenize(iter("1 + (23 * 45)"))), 1036)
        self.assertEqual(calc(tokenize(iter("(1 + 23) * 45"))), 1080)
        self.assertEqual(calc(tokenize(iter("((1 + 23) * 45) + 6"))), 1086)
        self.assertEqual(calc(tokenize(iter("1 + (23 * (45 + 6)) * (7 + 89)"))), 112704)


