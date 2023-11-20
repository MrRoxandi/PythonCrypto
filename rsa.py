import numeric


class RSA:
    __n: int
    __d: int
    __c: int

    def __init__(self, p: int, q: int) -> None:
        self.__n = p * q
        fi: int = (p - 1) * (q - 1)
        self.__d = numeric.generate_number(1, fi - 1)
        while numeric.gcd(self.__d, fi) != 1:
            self.__d = numeric.generate_number(1, fi - 1)
        self.__c = numeric.m_inverse(self.__d, fi)
        if self.__c < 0:
            self.__c += fi

    def get_n(self) -> int:
        return self.__n

    def get_d(self) -> int:
        return self.__d

    def get_c(self) -> int:
        return self.__c
