import random
import string
from datetime import datetime

random.seed(1024*datetime.now().timestamp())


def perturb(text, prob=0.05, letters=string.ascii_letters):
    chars = []
    for idx, c in enumerate(text):
        if (not c.isspace()) and random.random() < prob:
            op = random.choice(['a', 'r', 's'])
            if op == 'a':
                chars.append(get_random_char(letters))
                chars.append(c)
            elif op == 's':
                chars.append(get_random_char(letters))
        else:
            chars.append(c)
    return ''.join(chars)


def get_random_char(letters=string.ascii_letters):
    return random.choice(letters)


# print(perturb("Hello there! Is there a typo in this sentence? Are you sure?", 0.1))
# print(perturb("Hello there! Is there a typo in this sentence? Are you sure?", 0.1, "xyz"))
