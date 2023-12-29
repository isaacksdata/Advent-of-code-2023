from typing import List


def get_hash(s: str) -> int:
    """
    Get the HASH for a provided string

    ord() is used to get the ascii value for a particular character
    :param s: input string
    :return: hash value
    """
    v = 0
    for x in list(s):
        ascii_val = ord(x)
        v += ascii_val
        v *= 17
        v = v % 256
    return v


def solve(data: List[str], part: str = "a") -> int:
    """
    Solve the problem for day 1
    :param data: input data
    :param part: which part of the problem to solve - 'a' or 'b'
    :return: solution
    """
    if part == "a":
        return sum([get_hash(i) for i in data[0].split(",")])
    else:
        return 1
