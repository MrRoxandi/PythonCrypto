
import secrets
import hashlib
from rsa import RSA
from sympy import randprime, gcd, mod_inverse


def generate_prime(bits: int) -> int:
    return randprime(1 << bits, (1 << (bits + 1)) - 1)


class Candidate:
    """
    ---
    This is a class that can represent a Candidate

    Have vars:
    - name
    - hash

    ---
    Constructor: Candidate(name: str)
    """

    def __init__(self, name: str) -> None:
        self.__name = name
        self.__hash = int(hashlib.sha3_512(self.name.encode()).hexdigest(), 16)

    def __str__(self) -> str:
        return self.name

    def __hash__(self) -> int:
        return self.__hash

    @property
    def hash(self) -> int:
        """
        Returns a hash value of Candidate's name
        """
        return self.__hash

    @property
    def name(self) -> str:
        """
        Returns a str value of Candodate's name
        """
        return self.__name


class VoteErrorException(BaseException):
    ...


class SetSignErrorException(BaseException):
    ...


class CryptErrorException(BaseException):
    ...


class User:

    def __init__(self, name: str) -> None:
        self.__rnd = secrets.randbelow(1 << 512)
        self.__vote_info = 0
        self.__name = name
        self.__sign = 0

    @property
    def vote(self) -> int:
        return self.__vote_info

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str) -> str:
        self.__name = name

    @vote.setter
    def vote(self, person: Candidate) -> None:
        if self.__vote_info != 0:
            raise VoteErrorException(f"User {self.__name} already voted")
        print(f"{self.__name} -> [{person.name}]")
        hash_num = person.hash
        self.__vote_info = (hash_num << 512) + self.__rnd

    @property
    def sign(self) -> int:
        return self.__sign

    @sign.setter
    def sign(self, sign: int) -> None:
        if self.__sign != 0:
            raise SetSignErrorException(
                f"User {self.__name} already voted and have a sign")
        self.__sign = sign


class MainServerT:
    """
    This class represents a server where users can vote for candidates
    """

    def __init__(self) -> None:
        self._p, self_q = RSA.create_base_pair(1024)
        self._rsa = RSA(self._p, self_q)
        self._votes: list[(int, int)] = list()

    def add_vote(self, user: User) -> None:
        if self.is_voted(user):
            raise VoteErrorException(f"User {user.name} already voted\n")

        # Creating a numbers
        r, ir = RSA.create_inversed_pair(self._rsa.n - 1, self._rsa.n)

        h: int = int(hashlib.sha3_512(str(user.vote).encode()).hexdigest(), 16)
        s: int = (pow((h * pow(r, self._rsa.d, self._rsa.n)) % self._rsa.n,
                      self._rsa.c, self._rsa.n)) * ir % self._rsa.n
        # Safe check to validate crypt
        if h != pow(s, self._rsa.d, self._rsa.n):
            raise CryptErrorException(
                f"Error while crypting vote from user: {user.name}")

        self._votes.append((user.vote, s))
        user.sign = s

    def get_votes(self) -> list[(int, int)]:
        return self._votes

    @property
    def n(self) -> int: return self._rsa.n

    @property
    def key(self) -> int: return self._rsa.d

    def is_voted(self, user: User) -> bool:
        s = user.sign
        return any(item[1] == s for item in self._votes)

    def calculate_votes(self, candidates: list[Candidate]) -> list[(Candidate, int)]:
        return [
            (person, [vote[0] >> 512 for vote in self._votes].count(person.hash)) for person in candidates
        ]
