
import secrets, hashlib

from sympy import randprime, gcd, mod_inverse


def generate_prime(bits: int) -> int:
    return randprime(1 << bits, (1 << (bits + 1)) - 1)


class Candidate:
    
    def __init__(self, name: str) -> None:
        self.__name = name
        self.__hash = int(hashlib.sha3_512(self.name.encode()).hexdigest(), 16)

    def __str__(self) -> str:
        return self.name

    def __hash__(self) -> int:
        return self.__hash

    @property
    def hash(self) -> int:
        return self.__hash
    
    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, name: str) -> None:
        self.name = name

class User:

    def __init__(self) -> None:
        self.__rnd = secrets.randbelow(1 << 512)
        self.__vote_info = 0
        self.__sign = 0

    @property
    def vote(self) -> int:
        return self.__vote_info
    
    @vote.setter
    def vote(self, person: Candidate) -> None:
        hash_num = person.hash
        self.__vote_info = (hash_num << 512) + self.__rnd

    @property
    def sign(self) -> int:
        return self.__sign
    
    @sign.setter
    def sign(self, sign: int) -> None:
        self.__sign = sign


class MainServerT:

    def __init__(self) -> None:
        self._p = generate_prime(1024)
        self._q = generate_prime(1024)
        while self._q == self._p:
            self._q = generate_prime(1024)
        self._n = self._q * self._p
        fi = (self._p - 1) * (self._q - 1)
        self._c = secrets.randbelow(self._p - 1)
        while gcd(self._c, fi) != 1:
            self._c = secrets.randbelow(self._p - 1)
        self._d = mod_inverse(self._c, fi)
        self._votes: list[(int, int)] = list()

    def add_vote(self, user: User) -> None:
        if self.is_voted(user):
            raise Exception("You already voted\n")
        r: int = secrets.randbelow(self._n - 1)
        while gcd(r, self._n) != 1:
            r: int = secrets.randbelow(self._n - 1)
        ir: int = mod_inverse(r, self._n)
        h: int = int(hashlib.sha3_512(str(user.vote).encode()).hexdigest(), 16)
        h_: int = (h * pow(r, self._d, self._n)) % self._n
        s_: int = pow(h_, self._c, self._n)
        s: int = s_ * ir % self._n
        if h == pow(s, self._d, self._n):
            self._votes.append((user.vote, s))
            user.sign = s
        else:
            raise Exception("Error while crypt")

    def get_votes(self) -> list[(int, int)]:
        return self._votes

    def get_key(self) -> int:
        return self._d

    def get_n(self) -> int:
        return self._n

    def is_voted(self, user: User) -> bool:
        s = user.sign
        return any(item[1] == s for item in self._votes)
    
    def calculate_votes(self, candidates: list[Candidate]) -> list[(Candidate, int)]:
        results: list[(Candidate, int)] = [
            (person, [vote[0] >> 512 for vote in self._votes].count(person.hash)) for person in candidates
        ]
        return results
