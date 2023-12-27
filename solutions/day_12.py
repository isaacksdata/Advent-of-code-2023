from functools import cache
from itertools import chain
from itertools import groupby
from itertools import product
from typing import Generator
from typing import Iterable
from typing import List
from typing import Tuple
from typing import Union

import tqdm


def format_input(data: List[str], part: str = "a") -> List[Union[Tuple[str, List[int]], Tuple[str, Tuple[int, ...]]]]:
    """
    Format the input data for analysis

    If part == "b" then need to account for real input being 5x the given input.
    If part == "b" then the counts list is converted to tuple for caching
    :param data: input data
    :param part: the part of the AOC problem to solve
    :return: formatted data - input split into the string input and counts
    """
    split_data = [d.split(" ") for d in data]
    formatted_data: List[Union[Tuple[str, List[int]], Tuple[str, Tuple[int, ...]]]] = [
        (row, list(map(int, counts.split(",")))) for row, counts in split_data
    ]
    if part == "b":
        return [(((row + "?") * 5)[:-1], tuple(counts * 5)) for row, counts in formatted_data]
    return formatted_data


def generate_possibilities(row: str) -> product:
    """
    Create a generator of the possible combinations for unknown springs
    :param row: input data for a given row
    :return: generator of potential combinations
    """
    n = row.count("?")
    return product([".", "#"], repeat=n)


def get_contigous_ones(row: str) -> List[int]:
    """
    given an input string, groupby the # key and find the length of the groups.

    This results in a list of integers representing the length of contiguous groups of #
    :param row: input row
    :return: lengths of #s
    """
    return [sum(1 for _ in group) for key, group in groupby(list(row)) if key == "#"]


@cache
def analyse_segment(seg: str) -> List[List[int]]:
    """
    Analyse a segment of springs by brute force
    :param seg: imput string
    :return: list contigous #s for each possibility
    """
    return [get_contigous_ones(replace_unknowns(seg, list(s))) for s in generate_possibilities(seg)]


@cache
def analyse_row(row: str, springs: Tuple[int, ...], counter: int = 0) -> int:
    """
    Solve the problem using recursion and caching

    Iterate over the input row until ? is reached which is not followed by #. These are branch points so we split and
    repeat recursively along each possibility and keep a track of how many possibilities we have come across (result)
    :param row: input data row
    :param springs: counts
    :param counter: counter for number of possibilities
    :return: number of possibilities
    """
    if not springs:
        return "#" not in row
    current, springs = springs[0], springs[1:]
    for i in range(len(row) - sum(springs) - len(springs) - current + 1):
        if "#" in row[:i]:
            break
        if (nxt := i + current) <= len(row) and "." not in row[i:nxt] and row[nxt : nxt + 1] != "#":
            # if this is true it means we have reached a new branch point - there could be a 1 or 0 at this position
            # so need to keep iterating along both options
            # but no need to check it if the next position is # as we know whether it will be a 1 or 0 based on the
            # counts
            counter += analyse_row(row[nxt + 1 :], springs)
    return counter


def get_n_possible_combinations(row: str, counts: List[int]) -> int:
    """
    Get the number of possible combinations of row which fit counts by brute force
    :param row: input row
    :param counts: true counts
    :return: number of possibilities
    """
    # get possible combinations for each group
    res = [analyse_segment(s) for s in row.split(".") if s != ""]
    # combine the cgroups and check against the true
    options = [list(chain(*l)) for l in product(*res)]
    return len([x for x in options if x == counts])


def replace_unknowns(row: str, values: List[int]) -> str:
    """
    Replace unknowns "?" with "." or "#" to generate possible string
    :param row: input string with unknowns
    :param values: replacements for the unknowns - list with length equal to number of unknowns
    :return: string without unknowns
    """
    return "".join(str(values.pop(0)) if char == "?" else char for char in row)


def get_total_possible_combinations(data: List[str], part: str = "a") -> int:
    """
    Get total possble combinations for parts A or B
    :param data: input data
    :param part: the part of the problem to solve
    :return: number of combinations
    """
    f = format_input(data, part)
    if part == "a":
        ns = [get_n_possible_combinations(*d) for d in tqdm.tqdm(f)]
    else:
        ns = [analyse_row(*d) for d in tqdm.tqdm(f)]
    return sum(ns)


def solve(data: List[str], part: str = "a") -> int:
    """
    Solve the problem for day 1
    :param data: input data
    :param part: which part of the problem to solve - 'a' or 'b'
    :return: solution
    """
    if part == "a":
        return get_total_possible_combinations(data, part="a")
    else:
        return get_total_possible_combinations(data, part="b")
