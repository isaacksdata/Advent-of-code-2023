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


def find_vertical_mirror(puzzle: np.ndarray, old_ans: Optional[int] = None) -> Optional[int]:
    """
    Find a vertical mirror in the puzzle input

    Reflection must be True from the line all the way to the far left or far right.

    If no mirror line is found then return None
    :param puzzle: input puzzle
    :param old_ans: a previous answer which the real answer cannot be equal to
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
            elif old_ans is not None and mirror_line == old_ans - 1:
                mirror_line = None
                continue
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


def find_horizontal_mirror(puzzle: np.ndarray, old_ans: Optional[int] = None) -> Optional[int]:
    """
    Find a horizontal mirror in the puzzle input

    Reflection must be True from the line all the way to the top or bottom.

    If no mirror line is found then return None
    :param puzzle: input puzzle
    :param old_ans: a previous answer which the real answer cannot be equal to
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
            elif old_ans is not None and mirror_line == (old_ans / 100) - 1:
                mirror_line = None
                continue
            else:
                break
    return mirror_line


def solve_puzzle(puzzle: np.ndarray, old_ans: Optional[int] = None) -> int:
    """
    Solve a given puzzle by finding either a vertical or horizontal mirror line

    The answer should be the number of cols to left or number of rows (*100) above the mirror line
    If no mirror line is found then should return 0
    :param puzzle: input puzzle
    :param old_ans: a previous answer which the real answer cannot be equal to
    :return: answer for the puzzle
    """
    vm = find_vertical_mirror(puzzle, old_ans)
    if old_ans is not None and vm is not None:
        vm = None if vm + 1 == old_ans else vm
    if vm is None:
        hm = find_horizontal_mirror(puzzle, old_ans)
        if hm is None:
            answer = 0
        else:
            answer = (hm + 1) * 100
    else:
        answer = vm + 1
    return answer


def correct_smudge(puzzle: np.ndarray) -> int:
    """
    A smudge on the mirror which causes a different reflection line to be found - find the line after smudge correction

    Iterate over columns and rows to find possible indices for the smudge:
    These must be in a row or column which is different from another row/column in only one position
    Then iterate over the indices, do the replacement and find the one which gives a new position for the mirror

    :param puzzle: input puzzle
    :return: answer
    """
    # get the original answer for comparison
    first_ans = solve_puzzle(puzzle)

    # get a list of possible indices for the smudge
    idx = []
    # based on columns
    for i in range(puzzle.shape[0]):
        for j in range(i, puzzle.shape[0]):
            c1 = puzzle[i, :]
            c2 = puzzle[j, :]
            if np.sum(c1 == c2) == len(c1) - 1:
                col_id = int(np.argwhere(c1 != c2)[0][0])
                idx.extend([(i, col_id), (j, col_id)])

    # based on rows
    for i in range(puzzle.shape[1]):
        for j in range(i, puzzle.shape[1]):
            c1 = puzzle[:, i]
            c2 = puzzle[:, j]
            if np.sum(c1 == c2) == len(c1) - 1:
                row_id = int(np.argwhere(c1 != c2)[0][0])
                idx.extend([(row_id, i), (row_id, j)])

    # find the solution for each possible index
    ans = []
    for i, j in idx:
        replacement = "." if puzzle[i, j] == "#" else "#"
        p = puzzle.copy()
        p[i, j] = replacement
        a = solve_puzzle(p, old_ans=first_ans)
        if a > 0 and a != first_ans:
            ans.append(a)
    return [a for a in ans if a > 0 & a != first_ans][0]


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
        puzzles = extract_puzzles(data)
        return sum([correct_smudge(format_puzzle(p)) for p in puzzles])
