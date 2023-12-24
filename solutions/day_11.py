from itertools import combinations
from typing import List

import numpy as np


def format_input(data: List[str]) -> np.ndarray:
    """
    convert . to 0 and # to 1

    set to uint16 to handle galaxy numbers > 255
    :param data: input data
    :return: formatted array
    """
    arr = np.array([list(l) for l in data])
    mask = np.isin(arr, ["."])
    arr = np.where(mask, "0", arr)
    mask = np.isin(arr, ["#"])
    arr = np.where(mask, "1", arr)
    arr = arr.astype("uint16")
    return arr


def handle_expansion(arr: np.ndarray) -> np.ndarray:
    """
    Empty columns and rows should be duplicated

    np.sum() used across columns and rows and indices extracted for sum==0. Then insert empty col/row
    after each of these indices
    :param arr: input array
    :return: expanded array
    """
    empty_cols = [i for i, x in enumerate(np.sum(arr, axis=0)) if x == 0]
    empty_rows = [i for i, x in enumerate(np.sum(arr, axis=1)) if x == 0]

    for i, idx in enumerate(empty_cols):
        arr = np.insert(arr, idx + 1 + i, 0, axis=1)
    for i, idx in enumerate(empty_rows):
        arr = np.insert(arr, idx + 1 + i, 0, axis=0)
    return arr


def label_galaxies(arr: np.ndarray) -> np.ndarray:
    """
    Assign each galaxy a unique identifier

    :param arr: input array
    :return: labeled array
    """
    galaxies = np.argwhere(arr == 1).tolist()
    for i, c in enumerate(galaxies):
        arr[*c] = i + 1
    return arr


def shortest_path_between_ones(start: List[int], end: List[int]) -> int:
    """
    Calculate Euclidean distance between two 2D coordinates
    :param start: first coordinate
    :param end: second coordinate
    :return: Euclidean distance
    """
    return abs(start[0] - end[0]) + abs(start[1] - end[1])


def get_distances(arr: np.ndarray) -> List[int]:
    """
    Calculate distance between every pair of galaxies
    :param arr: input map of galaxies
    :return: list of distances
    """
    galaxies = [i for i in np.unique(arr) if i > 0]
    locations = {i: np.argwhere(arr == i).tolist()[0] for i in galaxies}
    pairs = list(combinations(galaxies, r=2))
    distances = [shortest_path_between_ones(locations[g1], locations[g2]) for g1, g2 in pairs]
    return distances


def find_total_distance(data: List[str]) -> int:
    """
    Find total distance between galaxies
    :param data: input data
    :return: sum of distances
    """
    arr = handle_expansion(format_input(data))
    arr = label_galaxies(arr)
    dists = get_distances(arr)
    return sum(dists)


def solve(data: List[str], part: str = "a") -> int:
    """
    Solve the problem for day 1
    :param data: input data
    :param part: which part of the problem to solve - 'a' or 'b'
    :return: solution
    """
    if part == "a":
        return find_total_distance(data)
    else:
        return 1
