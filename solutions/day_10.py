from collections import Counter
from itertools import chain
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np


symbols = ["|", "L", "J", "F", "-", ".", "Z"]  # 7 replaced with Z to avoid confusion with incrementing path


def gen_fig(arr: np.ndarray) -> None:
    """
    Generate an image to show the path from the array map
    :param arr: input array of symbols
    :return: void
    """
    mask = np.isin(arr, symbols)
    map_arr = np.where(mask, "0", arr)
    plt.imshow(map_arr.astype("uint16"))


def check_symbol(symbol: str, direction: str) -> bool:
    """
    Check to see if a symbol found in the map is valid for a given direction
    :param symbol: the symbol
    :param direction: the direction from current position
    :return: True if the symbol is valid else False
    """
    if symbol == ".":
        return False
    if direction == "top" and symbol in ["|", "F", "Z"]:
        return True
    if direction == "bottom" and symbol in ["|", "L", "J"]:
        return True
    if direction == "left" and symbol in ["-", "L", "F"]:
        return True
    if direction == "right" and symbol in ["-", "J", "Z"]:
        return True
    return False


def get_next_steps(
    arr: np.ndarray, i: str, current_positions: Optional[List[Tuple[int, int]]] = None
) -> List[Tuple[int, int]]:
    """
    Given the current map and current position(s) - find the next possible moves

    If no current _positions are provided - then find the current position using i which is a symbol to search for
    :param arr: the map
    :param i: symbol to search for
    :param current_positions: list of tuples indicating current positions along one side of the loop
    :return: List of possible next steps
    """
    current_positions = np.argwhere(arr == i).tolist() if current_positions is None else current_positions
    next_steps = []
    for idx in current_positions:
        mapping = {
            "left": (idx[0], idx[1] - 1) if idx[1] > 0 else None,
            "top": (idx[0] - 1, idx[1]) if idx[0] > 0 else None,
            "right": (idx[0], idx[1] + 1) if idx[1] + 1 < arr.shape[1] else None,
            "bottom": (idx[0] + 1, idx[1]) if idx[0] + 1 < arr.shape[0] else None,
        }
        direction: str
        c: Optional[Tuple[int, int]]
        for direction, c in mapping.items():
            if c is not None:
                if check_symbol(arr[c], direction):
                    next_steps.append(c)
    return next_steps


def is_numeric(value: str) -> bool:
    """
    Test if a string is a number e.g. "5" by trying to force to an integer
    :param value: input string
    :return: True if ValueError is not raised
    """
    try:
        int(value)
    except ValueError:
        return False
    else:
        return True


def take_steps(arr: np.ndarray, steps: Dict[int, List[Tuple[int, int]]], i: int) -> np.ndarray:
    """
    Given a dictionary of steps along each side of the loop - take the next possible steps

    This means replacing the next positions in the map with i which is np.max(arr) + 1
    :param arr: current map
    :param steps: a dict of next steps
    :param i: step number
    :return: updated map
    """
    for step in list(chain(*list(steps.values()))):
        arr[step] = i
    return arr


def check_steps_for_end(arr: np.ndarray, steps: Dict[int, List[Tuple[int, int]]]) -> bool:
    """
    Check to see if you have reached the point where the two sides of the loop meet

    This will be the point where there is a co-ordinate in both sides of the loop and that co-ordinate maps to a symbol
    which is not already numeric
    :param arr: input map
    :param steps: next possible positions
    :return: True if the end point has been reached
    """
    duplicates = set.intersection(*[set(v) for v in steps.values()])
    if len(duplicates) > 0:
        if not any([is_numeric(arr[j]) for j in duplicates]):
            return True
    return False


def find_path(arr: np.ndarray) -> Tuple[np.ndarray, int]:
    """
    Find the looping path through the array and stop at the point where the two sides of the loop meet
    :param arr: input map
    :return: mapped array, number of steps to meeting point
    """
    i = 0  # step counter
    start = np.where(arr == "S")
    arr[start] = 0
    steps = get_next_steps(arr, str(i))
    steps_dict = {0: [steps[0]], 1: [steps[1]]}
    while not check_steps_for_end(arr, steps_dict):
        i += 1
        arr = take_steps(arr, steps_dict, i)
        for key, pos in steps_dict.items():
            steps_dict[key] = get_next_steps(arr, str(i), pos)
    arr[steps[0]] = i + 1
    return arr, i + 1


def find_n_steps(data: List[str]) -> int:
    """
    Find the number of steps taken to reach the middle of the loop
    :param data: input data
    :return: number of steps
    """
    arr = np.array([list(l.replace("7", "Z")) for l in data])
    arr = arr.astype("<U5")  # allows strings upto 5 digits long in the array
    mapped_arr, i = find_path(arr)
    return i


def solve(data: List[str], part: str = "a") -> int:
    """
    Solve the problem for day 1
    :param data: input data
    :param part: which part of the problem to solve - 'a' or 'b'
    :return: solution
    """
    if part == "a":
        return find_n_steps(data)
    else:
        return 1
