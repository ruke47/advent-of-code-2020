from unittest import TestCase
import re

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
    total = get_val(tokens[0])
    token_iter = iter(tokens[1:])
    for token in token_iter:
        operator = token
        next_val = get_val(next(token_iter))
        if operator == "+":
            total += next_val
        elif operator == "*":
            total *= next_val
        else:
            raise ValueError(f"Unrecognized Operator: {operator}")    
    return total

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
        self.assertEqual(calc(tokenize(iter("1 + 2 * 3 + 4"))), 13)
        self.assertEqual(calc(tokenize(iter("1 + 23 * 45"))), 1080)
        self.assertEqual(calc(tokenize(iter("1 + (23 * 45)"))), 1036)
        self.assertEqual(calc(tokenize(iter("(1 + 23) * 45"))), 1080)
        self.assertEqual(calc(tokenize(iter("((1 + 23) * 45) + 6"))), 1086)
        self.assertEqual(calc(tokenize(iter("1 + (23 * (45 + 6)) * (7 + 89)"))), 112704)


