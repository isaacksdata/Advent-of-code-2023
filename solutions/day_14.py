from typing import List

import matplotlib.pyplot as plt
import numpy as np


def view_map(puzzle: np.ndarray) -> None:
    """
    View the map as an image
    :param puzzle: input puzzle array
    :return: void
    """
    arr = puzzle.copy()
    mask = np.isin(arr, ["."])
    arr = np.where(mask, "0", arr)
    mask = np.isin(arr, ["#"])
    arr = np.where(mask, "1", arr)
    mask = np.isin(arr, ["O"])
    arr = np.where(mask, "2", arr)
    plt.imshow(arr.astype("uint8"))


def roll_north(arr: np.ndarray, ball: List[int]) -> np.ndarray:
    """
    Roll a round ball starting at ball towards the top of the array
    :param arr: the map
    :param ball: the starting position of the ball
    :return: new map after rolling the ball
    """
    if ball[0] == 0:  # nowhere to roll to!
        return arr
    while arr[ball[0] - 1, ball[1]] == ".":
        arr[ball[0] - 1, ball[1]] = "O"
        arr[ball[0], ball[1]] = "."
        if ball[0] - 1 < 1:
            break
        ball = [ball[0] - 1, ball[1]]
    return arr


def use_north_lever(arr: np.ndarray) -> np.ndarray:
    """
    Roll all round balls ("O") towards the top of the array
    :param arr: input map
    :return: new map after rolling
    """
    round_balls = np.argwhere(arr == "O")
    for ball in round_balls:
        arr = roll_north(arr, ball)
    return arr


def calculate_load(arr: np.ndarray) -> int:
    """
    Determine the load of the round balls where balls further towards the top contribute more to the load
    :param arr: input map
    :return: total load
    """
    return sum([arr.shape[0] - r[0] for r in np.argwhere(arr == "O")])


def solve(data: List[str], part: str = "a") -> int:
    """
    Solve the problem for day 1
    :param data: input data
    :param part: which part of the problem to solve - 'a' or 'b'
    :return: solution
    """
    if part == "a":
        arr = np.array([list(l) for l in data])
        return calculate_load(use_north_lever(arr))
    else:
        return 1
