from itertools import combinations
from typing import List
from typing import Tuple

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


def handle_expansion(arr: np.ndarray, expansion_rate: int = 1) -> Tuple[np.ndarray, List[int], List[int]]:
    """
    Empty columns and rows should be duplicated

    np.sum() used across columns and rows and indices extracted for sum==0. Then insert empty col/row
    after each of these indices
    :param arr: input array
    :param expansion_rate: the number of empty rows/cols to replace each empty row/col with
    :return: expanded array
    """
    empty_cols = [i for i, x in enumerate(np.sum(arr, axis=0)) if x == 0]
    empty_rows = [i for i, x in enumerate(np.sum(arr, axis=1)) if x == 0]

    if expansion_rate == 1:
        for i, idx in enumerate(empty_cols):
            arr = np.insert(
                arr,
                idx + 1 + i * (expansion_rate - 1),
                np.zeros(
                    (
                        expansion_rate - 1,
                        arr.shape[0],
                    )
                ),
                axis=1,
            )
        for i, idx in enumerate(empty_rows):
            arr = np.insert(
                arr, idx + 1 + i * (expansion_rate - 1), np.zeros((expansion_rate - 1, arr.shape[1])), axis=0
            )
    return arr, empty_rows, empty_cols


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


def shortest_path_between_ones(
    start: List[int], end: List[int], empty_rows: List[int], empty_cols: List[int], expansion_rate: int
) -> int:
    """
    Calculate Euclidean distance between two 2D coordinates
    :param start: first coordinate
    :param end: second coordinate
    :param empty_rows: indices of empty rows in the original array
    :param empty_cols: indices of empty cols in the original array
    :param expansion_rate: the number of empty rows/cols to replace each empty row/col with
    :return: Euclidean distance
    """
    if expansion_rate == 1:
        return abs(start[0] - end[0]) + abs(start[1] - end[1])
    else:
        empty_cols_before_start = [x for x in empty_cols if x < start[1]]
        empty_rows_before_start = [x for x in empty_rows if x < start[0]]
        start = [
            start[0] + len(empty_rows_before_start) * (expansion_rate - 1),
            start[1] + len(empty_cols_before_start) * (expansion_rate - 1),
        ]

        empty_cols_before_end = [x for x in empty_cols if x < end[1]]
        empty_rows_before_end = [x for x in empty_rows if x < end[0]]
        end = [
            end[0] + len(empty_rows_before_end) * (expansion_rate - 1),
            end[1] + len(empty_cols_before_end) * (expansion_rate - 1),
        ]

        raw_dist = abs(start[0] - end[0]) + abs(start[1] - end[1])
        return raw_dist


def get_distances(arr: np.ndarray, empty_rows: List[int], empty_cols: List[int], expansion_rate: int) -> List[int]:
    """
    Calculate distance between every pair of galaxies
    :param arr: input map of galaxies
    :param empty_rows: indices of empty rows in the original array
    :param empty_cols: indices of empty cols in the original array
    :param expansion_rate: the number of empty rows/cols to replace each empty row/col with
    :return: list of distances
    """
    galaxies = [i for i in np.unique(arr) if i > 0]
    locations = {i: np.argwhere(arr == i).tolist()[0] for i in galaxies}
    pairs = list(combinations(galaxies, r=2))
    distances = [
        shortest_path_between_ones(locations[g1], locations[g2], empty_rows, empty_cols, expansion_rate)
        for g1, g2 in pairs
    ]
    return distances


def find_total_distance(data: List[str], expansion_rate: int = 1) -> int:
    """
    Find total distance between galaxies
    :param data: input data
    :param expansion_rate: the number of empty rows/cols to replace each empty row/col with
    :return: sum of distances
    """
    arr, empty_rows, empty_cols = handle_expansion(format_input(data), expansion_rate)
    arr = label_galaxies(arr)
    dists = get_distances(arr, empty_rows, empty_cols, expansion_rate)
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
        return find_total_distance(data, expansion_rate=1000000)
