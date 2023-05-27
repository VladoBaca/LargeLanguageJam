import random
import string
from datetime import datetime


def perturb(text, prob=0.05):
    random.seed(datetime.now().timestamp())
    chars = list(text)
    for idx, c in enumerate(chars):
        if random.random() < prob:
            chars[idx] = get_random_char()
    return ''.join(chars)


def get_random_char():
    return random.choice(string.ascii_letters)


print(perturb("Hello there! Is there a typo in this sentence? Are you sure?"))
