import random


def create_seq(length: int, filler: chr) -> str:
    res: str = ""
    for _ in range(length):
        res += filler
    return res


def generate_number(lower_bound: int, upper_bound: int) -> int:
    if lower_bound > upper_bound:
        raise "Invalid bounds"
    return random.randint(lower_bound, upper_bound)


def generate_prime(lower_bound: int, upper_bound: int) -> int:
    while True:
        candidate: int = generate_number(lower_bound, upper_bound)
        candidate |= 1
        if is_prime(candidate, 25):
            return candidate


def power_mod(base: int, power: int, mod: int) -> int:
    return pow(base, power, mod)


def gcd(a: int, b: int) -> int:
    while b != 0:
        tmp: int = a % b
        a = b
        b = tmp
    return a


def is_prime(number: int, iterations: int) -> bool:
    if number == 2 or number == 3:
        return True
    if number % 2 == 0 or number % 3 == 0:
        return False
    for _ in range(iterations):
        check: int = generate_number(1, number - 1)
        if pow(check, number - 1, number) != 1:
            return False
    return True


class Int3D:
    def __init__(
            self,
            first: int,
            second: int,
            third: int
    ) -> None:
        self.first = first
        self.second = second
        self.third = third


def Euclid_alg(a: int, b: int) -> Int3D:
    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = b // a, b % a
        m, n = x - u * q, y - v * q
        b, a, x, y, u, v = a, r, u, v, m, n
    r_gcd: int = b
    return Int3D(r_gcd, x, y)


def m_inverse(a: int, p: int) -> int:
    inverse: int = Euclid_alg(a, p).second
    if inverse < 0:
        inverse += p
    return inverse
