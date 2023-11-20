import secrets, hashlib, sympy


def generate_prime(bits: int) -> int:
    return sympy.randprime(1 << bits, (1 << (bits + 1)) - 1)


class Candidate:
    __name: str 

    def __init__(self, name: str) -> None:
        self.__name = name

    def __str__(self) -> str:
        return self.name

    def __hash__(self) -> int:
        return int(hashlib.sha3_512(self.name.encode()).hexdigest(), 16)

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
        hash_num = person.__hash__()
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
        while sympy.gcd(self._c, fi) != 1:
            self._c = secrets.randbelow(self._p - 1)
        self._d = sympy.mod_inverse(self._c, fi)
        self._votes: set[(int, int)] = set()

    def add_vote(self, user: User) -> None:
        if self.is_voted(user):
            raise Exception("You already voted\n")
        r: int = secrets.randbelow(self._n - 1)
        while sympy.gcd(r, self._n) != 1:
            r: int = secrets.randbelow(self._n - 1)
        ir: int = sympy.mod_inverse(r, self._n)
        h: int = int(hashlib.sha3_512(str(user.vote).encode()).hexdigest(), 16)
        h_: int = (h * pow(r, self._d, self._n)) % self._n
        s_: int = pow(h_, self._c, self._n)
        s: int = s_ * ir % self._n
        if h == pow(s, self._d, self._n):
            self._votes.add((user.vote, s))
            user.sign = s
        else:
            raise Exception("Error while crypt")

    def get_votes(self) -> set[(int, int)]:
        return self._votes

    def get_key(self) -> int:
        return self._d

    def get_n(self) -> int:
        return self._n

    def is_voted(self, user: User) -> bool:
        s = user.sign
        return any(item[1] == s for item in self._votes)
    
    def calculate_votes(self, users: list[User], candidates: list[Candidate]) -> list[Candidate]:
        results: list[Candidate] = [
            candidate for user in users if self.is_voted(user)
            for candidate in candidates
            if ( user.vote >> 512 ) == int(hashlib.sha3_512(candidate.name.encode()).hexdigest(), 16)
        ]
        return results