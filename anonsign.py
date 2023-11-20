import numeric
import hashlib


class Candidate:
    __name: str

    def __init__(self, name: str) -> None:
        self.__name = name

    def get_name(self) -> str:
        return self.__name

    def set_name(self, name: str) -> None:
        self.__name = name


class User:
    __rnd: int
    __vote_info: int = 0
    __sign: int = 0

    def __init__(self) -> None:
        self.__rnd = numeric.generate_number(1 << 512, (1 << 513) - 1)

    def vote(self, person: Candidate) -> None:
        hash_num = int(hashlib.sha3_512(person.get_name().encode()).hexdigest(), 16)
        self.__vote_info = (self.__rnd << 512) + hash_num

    def get_vote(self) -> int:
        return self.__vote_info

    def set_sing(self, sign: int) -> None:
        self.__sign = sign

    def get_sing(self) -> int:
        return self.__sign


class MainServerT:
    _p: int
    _q: int
    _n: int
    _c: int
    _d: int
    _votes: set[(int, int)] = set()

    def __init__(self) -> None:
        self._p = numeric.generate_prime(1 << 1024, (1 << 1025) - 1)
        self._q = numeric.generate_prime(1 << 1024, (1 << 1025) - 1)
        while self._q == self._p:
            self._q = numeric.generate_prime(1 << 1024, (1 << 1025) - 1)
        self._n = self._q * self._p
        fi = (self._p - 1) * (self._q - 1)
        self._c = numeric.generate_number(1, self._p - 1)
        while numeric.gcd(self._c, fi) != 1:
            self._c = numeric.generate_number(1, self._p - 1)
        self._d = numeric.m_inverse(self._c, fi)

    def vote(self, user: User) -> None:
        if self.is_voted(user):
            raise "You already voted\n"
        r: int = numeric.generate_number(1, self._n - 1)
        while numeric.gcd(r, self._n) != 1:
            r: int = numeric.generate_number(1, self._n - 1)
        ir: int = numeric.m_inverse(r, self._n)
        h: int = int(hashlib.sha3_512(str(user.get_vote()).encode()).hexdigest(), 16)
        h_: int = (h * pow(r, self._d, self._n)) % self._n
        s_: int = pow(h_, self._c, self._n)
        s: int = s_ * ir % self._n
        if h == pow(s, self._d, self._n):
            self._votes.add((user.get_vote(), s))
            user.set_sing(s)
        else:
            raise "Error while crypt"

    def get_votes(self) -> set[(int, int)]:
        return self._votes

    def get_key(self) -> int:
        return self._d

    def get_n(self) -> int:
        return self._n

    def is_voted(self, user: User) -> bool:
        s = user.get_sing()
        for item in self._votes:
            if item[1] == s:
                return True
            else: continue
        return False
    
    def calculate_votes(self, users: list[User], candidates: list[Candidate]) -> list[Candidate]:
        results: list[Candidate] = []
        for user in users:
            if self.is_voted(user):
                h = (user.get_vote()) % (1 << 512)
                for candidate in candidates:
                    if h != int(hashlib.sha3_512(candidate.get_name().encode()).hexdigest(), 16):
                        continue
                    else: results.append(candidate)
            else: continue
        return results