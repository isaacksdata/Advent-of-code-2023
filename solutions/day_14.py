from typing import List
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm


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


def roll(arr: np.ndarray, ball: List[int], direction: str) -> np.ndarray:
    match direction:
        case "north":
            if ball[0] == 0:
                return arr
            while arr[ball[0] - 1, ball[1]] == ".":
                arr[ball[0] - 1, ball[1]] = "O"
                arr[ball[0], ball[1]] = "."
                if ball[0] - 1 < 1:
                    break
                ball = [ball[0] - 1, ball[1]]
        case "south":
            if ball[0] == arr.shape[0] - 1:
                return arr
            while arr[ball[0] + 1, ball[1]] == ".":
                arr[ball[0] + 1, ball[1]] = "O"
                arr[ball[0], ball[1]] = "."
                if ball[0] + 1 == arr.shape[0] - 1:
                    break
                ball = [ball[0] + 1, ball[1]]
        case "east":
            if ball[1] == arr.shape[1] - 1:
                return arr
            while arr[ball[0], ball[1] + 1] == ".":
                arr[ball[0], ball[1] + 1] = "O"
                arr[ball[0], ball[1]] = "."
                if ball[1] + 1 == arr.shape[1] - 1:
                    break
                ball = [ball[0], ball[1] + 1]
        case "west":
            if ball[1] == 0:
                return arr
            while arr[ball[0], ball[1] - 1] == ".":
                arr[ball[0], ball[1] - 1] = "O"
                arr[ball[0], ball[1]] = "."
                if ball[1] - 1 < 1:
                    break
                ball = [ball[0], ball[1] - 1]
        case _:
            raise ValueError("Unexpected direction!")
    return arr


def run_cycle(arr_tup: Tuple[str, ...], shape: Tuple[int, ...]) -> np.ndarray:
    """
    Execute a cycle of titling N, W, S, E

    Note that order moving the round rocks is different for different tilting directions
    :param arr_tup: input array as a tuple of strs
    :param shape: shape of the array
    :return: updated array
    """
    arr = np.array(arr_tup).reshape(shape)
    for d in ["north", "west", "south", "east"]:
        round_balls = np.argwhere(arr == "O").tolist()
        match d:
            case "south":
                round_balls = sorted(round_balls, key=lambda x: x[0], reverse=True)
            case "east":
                round_balls = sorted(round_balls, key=lambda x: x[1], reverse=True)
            case "west":
                round_balls = sorted(round_balls, key=lambda x: x[1], reverse=False)
        for ball in round_balls:
            arr = roll(arr, ball, d)
    return arr


def run_cycles(arr: np.ndarray, n: int) -> np.ndarray:
    """
    Run N cycles - when running the cycles, we check to see if the array gets into a loop

    If a loop is detected, then can stop iterating and calculate where in the loop would stop after remaining steps
    :param arr: input starting array
    :param n: number of cycles to execute
    :return: final array
    """
    arrs: List[np.ndarray] = [arr]
    i = 0
    for i in tqdm(range(n)):
        arr = run_cycle(tuple(arr.flatten()), arr.shape)
        if any(np.array_equal(arr, a) for a in arrs):
            break
        else:
            arrs.append(arr)
    first_el = [i for i, a in enumerate(arrs) if np.array_equal(a, arr)][0]
    loop = arrs[first_el:]
    final_idx = (n - i) % len(loop)
    return loop[final_idx - 1]


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
        arr = np.array([list(l) for l in data])
        return calculate_load(run_cycles(arr, 1000000000))
