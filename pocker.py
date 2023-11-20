import random, numeric
from typing import Optional


class Card:

    def __init__(self, number: int) -> None:
        self.__value = number

    def get_number(self) -> int:
        return self.__value

    def use_key(self, key: int, p: int) -> None:
        self.__value = pow(self.__value, key, p)

    def __str__(self) -> str:
        return str(self.get_number())

    def __eq__(self, __other: object) -> bool:
        return self.__value == __other.__value


class Deck:

    def __init__(self, size: int) -> None:
        self.__value: list[Card] = []
        for n in range(2, size + 2):
            self.__value.append(Card(n))

    def __str__(self) -> str:
        res: str = ""
        for item in self.__value:
            res += item.__str__() + " "
        return res

    def __eq__(self, __value: object) -> bool:
        return self.__value == __value.__value

    def insert_card(self, item: Card) -> None:
        self.__value.append(item)

    def pick_card(self, n: int = 0) -> Optional[Card]:
        n = numeric.generate_number(0, len(self.__value)) if n == 0 else n
        if n < len(self.__value):
            res = self.__value[n]
            self.__value.remove(res)
            return res
        else:
            return None

    def shuffle(self) -> None:
        random.shuffle(self.__value)

    def use_key(self, key: int, p: int) -> None:
        for card in self.__value:
            card.use_key(key, p)


class Player:
    __name: str
    __keys: list[int]
    __load_out: list[Card]

    def __init__(self, p: int, name: str = "") -> None:
        d = numeric.generate_prime(1, p - 1)
        while numeric.gcd(d, p - 1) != 1:
            d = numeric.generate_prime(1, p - 1)
        c = numeric.m_inverse(d, p - 1)
        self.__keys = [c, d]
        self.__load_out = []
        self.__name = name

    def __str__(self) -> str:
        res: str = f"Player: [{self.__name}]: [ "
        for item in self.__load_out:
            res += item.__str__() + " "
        return res + "]"

    def get_cards(self) -> list[Card]:
        return self.__load_out

    def add_card(self, card: Card) -> None:
        self.__load_out.append(card)

    def use_key(self, key: int, p: int) -> None:
        for item in self.__load_out:
            item.use_key(key, p)

    def get_name(self, name: str) -> None:
        self.__name = name

    def get_key(self, n: int) -> int:
        if n > 1 or n < 0:
            raise "Invalid key number"
        return self.__keys[n]


class GameP:
    __p: int
    __deck: Deck
    __players: list[Player] = []

    def __init__(self, size: int, mod: int) -> None:
        self.__p = mod
        self.__deck = Deck(52)
        self.__players: list[Player] = []
        for i in range(size):
            self.__players.append(Player(mod, str(i)))

    def get_players(self) -> list[Player]:
        return self.__players

    def get_deck(self) -> Deck:
        return self.__deck

    def get_param(self) -> int:
        return self.__p


def Mental_Pocker(n: int) -> None:
    q = numeric.generate_prime(1 << 32, 1 << 64)
    p = 2 * q + 1
    while not numeric.is_prime(p, 25):
        q = numeric.generate_prime(1 << 32, 1 << 64)
        p = 2 * q + 1
    game = GameP(n, p)
    players = game.get_players()
    for pl in players:
        game.get_deck().shuffle()
        game.get_deck().use_key(pl.get_key(0), game.get_param())
    for pl in players:
        for _ in range(2):
            pl.add_card(game.get_deck().pick_card())
    for pl in players:
        for card in pl.get_cards():
            for e_pl in players:
                card.use_key(e_pl.get_key(1), game.get_param())
        print(pl)
