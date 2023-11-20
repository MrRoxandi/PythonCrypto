import random
from convert import convert
from math import ceil, log2


def Vernam_key(number: int) -> int:
    length: int = ceil(log2(number))
    res: int = int('0', 2)
    for _ in range(length):
        res += random.randint(0, 1)
    return convert(res, 2, 10)


def Vernam_alg(number: int, key: int) -> int:
    return number ^ key
