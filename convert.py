def convert(number: int, from_base: int, to_base: int) -> int:
    temp: str = ""
    while number > 0:
        temp += str(number % from_base)
        number //= from_base
    return int(temp, to_base)
