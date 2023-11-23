
from sympy import randprime, gcd, mod_inverse
from secrets import randbelow


class RSA:

    def __init__(self, p: int, q: int) -> None:
        self.__n = p * q
        fi: int = (p - 1) * (q - 1)
        self.__d = randbelow(fi - 1)
        while gcd(self.__d, fi) != 1:
            self.__d = randbelow(fi - 1)
        self.__c = mod_inverse(self.__d, fi)

    @property
    def n(self) -> int:
        return self.__n

    @property
    def c(self) -> int:
        return self.__c

    @property
    def d(self) -> int:
        return self.__d

    @staticmethod
    def create_base_pair(bits: int) -> (int, int):
        q, p = randprime(1 << bits, (1 << bits + 1) -
                         1), randprime(1 << bits, (1 << bits + 1) - 1)
        while q == p:
            q = randprime(1 << bits, (1 << bits + 1) - 1)
        return (q, p)

    @staticmethod
    def create_inversed_pair(upper_bound: int, mod: int) -> (int, int):
        """
        # Create a tuple with number and his inverse by mod
        ---
        Return (p, ip) tuple with this params:
        1. gcd(p, mod) = 1
        2. (p * ip) % (mod) = 1
        """
        p = randbelow(upper_bound)
        while gcd(p, mod) != 1:
            p = randbelow(upper_bound)
        ip = mod_inverse(p, mod)
        return (p, ip)
