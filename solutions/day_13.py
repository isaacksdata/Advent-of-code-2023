from itertools import groupby
from typing import List
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np


def view_puzzle(puzzle: np.ndarray) -> None:
    """
    Visualise the puzzle input as a 2D image
    :param puzzle: input puzzle
    :return: void
    """
    arr = puzzle.copy()
    mask = np.isin(arr, ["."])
    arr = np.where(mask, "0", arr)
    mask = np.isin(arr, ["#"])
    arr = np.where(mask, "1", arr)
    plt.imshow(arr.astype("uint8"))


def extract_puzzles(data: List[str]) -> List[List[str]]:
    """
    Extract the list of puzzles (each puzzle represents one mirror)
    :param data: input data
    :return: list of puzzles where each puzzle is a list of strings
    """
    return [list(group) for key, group in groupby(data, key=lambda x: x == "") if not key]


def format_puzzle(puzzle_data: List[str]) -> np.ndarray:
    """
    Convert list of strings format to numpy array
    :param puzzle_data: input puzzle
    :return: puzzle as a numpy array (2D)
    """
    return np.array([list(l) for l in puzzle_data])


def find_vertical_mirror(puzzle: np.ndarray) -> Optional[int]:
    """
    Find a vertical mirror in the puzzle input

    Reflection must be True from the line all the way to the far left or far right.

    If no mirror line is found then return None
    :param puzzle: input puzzle
    :return: index of the column to the left of the line or None
    """
    mirror_line = None
    for i in range(puzzle.shape[1] - 1):
        c1 = puzzle[:, i]
        c2 = puzzle[:, i + 1]
        if check_equal(c1, c2):  # this means that cols i and i+1 are equal and are possible mirror line
            d = 0
            while check_equal(c1, c2):
                d += 1
                if i - d < 0:
                    mirror_line = i
                    break
                try:
                    c1 = puzzle[:, i - d]
                    c2 = puzzle[:, i + 1 + d]
                except IndexError:
                    mirror_line = i
                    break
                else:
                    pass
            if mirror_line is None:
                continue  # check for another possible mirror line
            else:
                break
    return mirror_line


def check_equal(x: np.ndarray, y: np.ndarray) -> bool:
    """
    Check if two arrays are equal
    :param x: array 1
    :param y: array 2
    :return: True if equal else False
    """
    return bool(np.all(x == y))


def find_horizontal_mirror(puzzle: np.ndarray) -> Optional[int]:
    """
    Find a horizontal mirror in the puzzle input

    Reflection must be True from the line all the way to the top or bottom.

    If no mirror line is found then return None
    :param puzzle: input puzzle
    :return: index of the row above the line or None
    """
    mirror_line = None
    for i in range(puzzle.shape[0] - 1):
        c1 = puzzle[i, :]
        c2 = puzzle[i + 1, :]
        if check_equal(c1, c2):  # this means that rows i and i+1 are equal and are possible mirror line
            d = 0
            while check_equal(c1, c2):
                d += 1
                if i - d < 0:
                    mirror_line = i
                    break
                try:
                    c1 = puzzle[i - d, :]
                    c2 = puzzle[i + 1 + d, :]
                except IndexError:
                    mirror_line = i
                    break
                else:
                    pass
            if mirror_line is None:
                continue
            else:
                break
    return mirror_line


def solve_puzzle(puzzle: np.ndarray) -> int:
    """
    Solve a given puzzle by finding either a vertical or horizontal mirror line

    The answer should be the number of cols to left or number of rows (*100) above the mirror line
    If no mirror line is found then should return 0
    :param puzzle: input puzzle
    :return: answer for the puzzle
    """
    vm = find_vertical_mirror(puzzle)
    if vm is None:
        hm = find_horizontal_mirror(puzzle)
        if hm is None:
            answer = 0
        else:
            answer = (hm + 1) * 100
    else:
        answer = vm + 1
    return answer


def solve(data: List[str], part: str = "a") -> int:
    """
    Solve the problem for day 1
    :param data: input data
    :param part: which part of the problem to solve - 'a' or 'b'
    :return: solution
    """
    if part == "a":
        puzzles = extract_puzzles(data)
        return sum([solve_puzzle(format_puzzle(p)) for p in puzzles])
    else:
        return 1


# if __name__ == "__main__":
#     test_data = [
#         "#.##..##.",
#         "..#.##.#.",
#         "##......#",
#         "##......#",
#         "..#.##.#.",
#         "..##..##.",
#         "#.#.##.#.",
#         "",
#         "#...##..#",
#         "#....#..#",
#         "..##..###",
#         "#####.##.",
#         "#####.##.",
#         "..##..###",
#         "#....#..#",
#     ]
#
#     from solutions.utilities import (
#         get_puzzle,
#         submit_answer,
#         save_sample_data,
#         format_input_data,
#         run_and_measure,
#     )
#     data = get_puzzle(year=2023, day=13)
#     test_data = format_input_data(data)
#
#     p = ['....#...####..#',
#  '.###.....####.#',
#  '###.#.##..#.#..',
#  '#.#.######...#.',
#  '#.#####.#..#.#.',
#  '...#......#.##.',
#  '####....#......',
#  '#.#..#..#####.#',
#  '##..#.##...#.##',
#  '...#.#.###.###.',
#  '..####.##...#.#',
#  '..####.##...#.#',
#  '...#.#..##.###.',
#  '...#.#..##.###.',
#  '..####.##...#.#',
#  '..####.##...#.#',
#  '...#.#.###.###.']
#     solve_puzzle(format_puzzle(p))
#     solve(test_data)
