"""Solution for AOC 2023 Day 1"""
import re
from typing import List
from typing import Union

import numpy as np

mapping = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def extract_numbers_from_string(string: str) -> List[int]:
    """
    Extract integers from a string
    :param string: input string
    :return: a list of numbers found in the string
    """
    return re.findall(r"\d", string)


def calibrate_string(string: str) -> int:
    """
    Calibrate the string for part A of day 1 by extracting the first and last integers from a string
    :param string: input string
    :return: output integer
    """
    numbers = extract_numbers_from_string(string)
    return int(f"{numbers[0]}{numbers[-1]}")


def find_pattern_indices(input_string: str, pattern: str, first: bool = True) -> int:
    """
    Return the first index of either the first or last sequence of a pattern in a string
    :param input_string: string to find patterns in
    :param pattern: the pattern to find
    :param first: If true, then search from left, else search from right (last match)
    :return: index of the start of the match
    """
    if first:
        idx = input_string.find(pattern)
    else:
        idx = input_string.rfind(pattern)
    return idx


def calibrate_string_with_letters(s: str) -> int:
    """
    Calibration of the string taking into account numbers indicated using letters
    :param s: input string
    :return: the number derived from the string
    """
    patterns = [*[str(i) for i in mapping], *[str(i) for i in mapping.values()]]
    first_idx = [find_pattern_indices(s, p, True) if p in s else np.nan for p in patterns]
    last_idx = [find_pattern_indices(s, p, False) if p in s else np.nan for p in patterns]
    idx_min = int(np.nanargmin(first_idx))
    idx_max = int(np.nanargmax(last_idx))
    if patterns[idx_min] in mapping:
        d0: Union[int, str] = mapping[patterns[idx_min]]
    else:
        d0 = patterns[idx_min]
    if patterns[idx_max] in mapping:
        d1: Union[int, str] = mapping[patterns[idx_max]]
    else:
        d1 = str(patterns[idx_max])
    return int(f"{d0}{d1}")


def solve(data: List[str], part: str = "a") -> int:
    """
    Solve the problem for day 1
    :param data: input data
    :param part: which part of the problem to solve - 'a' or 'b'
    :return: solution
    """
    if part == "a":
        values = [calibrate_string(i) for i in data]
    elif part == "b":
        values = [calibrate_string_with_letters(i) for i in data]
    else:
        raise ValueError("Incorrect part!")
    return sum(values)
