from typing import List

import numpy as np


def possible_move(arr: np.ndarray, pos: List[int]) -> bool:
    """
    Check to see if a move is within the boundaries of the array
    :param arr: the map
    :param pos: the position to move to
    :return: True if the position is within the array else False
    """
    return not (pos[0] < 0 or pos[0] > arr.shape[0] - 1 or pos[1] < 0 or pos[1] > arr.shape[1] - 1)


def trace_beam(
    arr: np.ndarray, current_pos: List[int], next_pos: List[int], beam_starts: List[List[int]]
) -> List[List[int]]:
    """
    Trace a beam until no further moves or possible or until the start of beam already logged is reached
    :param arr: map
    :param current_pos: the current position co-ordinate
    :param next_pos: the next position co-ordinate
    :param beam_starts: a list of already logged beam starting points - used to stop infinite loops
    :return:
    """
    energised: List[List[int]] = []

    # this check is to avoid tracking positions with negative indices
    if np.all([0 <= x < d for x, d in zip(current_pos, arr.shape)]):
        energised.append(current_pos)

    # begin following the beam
    while possible_move(arr, next_pos):
        # if this check is True then reached the start of a previously logged loop so can break off
        if next_pos in beam_starts:
            break
        energised.append(next_pos)
        next_char = arr[next_pos[0], next_pos[1]]
        match next_char:
            case ".":  # empty space so continue straight
                diff = np.array(next_pos) - np.array(current_pos)
                current_pos = next_pos
                next_pos = (np.array(next_pos) + diff).tolist()
            case "\\":  # a mirror so reflect at 90 degrees to current direction
                diff = (np.array(next_pos) - np.array(current_pos)).tolist()
                current_pos = next_pos
                match diff:
                    case [0, 1]:
                        # turn the beam downwards as beam is travelling right
                        next_pos = (np.array(next_pos) + np.array([1, 0])).tolist()
                    case [-1, 0]:
                        # turn the beam to left as beam is travelling up
                        next_pos = (np.array(next_pos) + np.array([0, -1])).tolist()
                    case [0, -1]:
                        # turn the beam up as beam is travelling left
                        next_pos = (np.array(next_pos) + np.array([-1, 0])).tolist()
                    case [1, 0]:
                        # turn the beam to right as beam is travelling down
                        next_pos = (np.array(next_pos) + np.array([0, 1])).tolist()
            case "/":  # a mirror so reflect at 90 degrees to current direction
                diff = (np.array(next_pos) - np.array(current_pos)).tolist()
                current_pos = next_pos
                match diff:
                    case [0, 1]:
                        # turn the beam upwards as beam is travelling right
                        next_pos = (np.array(next_pos) + np.array([-1, 0])).tolist()
                    case [-1, 0]:
                        # turn the beam to right as beam is travelling up
                        next_pos = (np.array(next_pos) + np.array([0, 1])).tolist()
                    case [0, -1]:
                        # turn the beam down as beam is travelling left
                        next_pos = (np.array(next_pos) + np.array([1, 0])).tolist()
                    case [1, 0]:
                        # turn the beam to left as beam is travelling down
                        next_pos = (np.array(next_pos) + np.array([0, -1])).tolist()
            case "-":  # a splitter
                if current_pos[0] == next_pos[0]:
                    # treat this as empty space and no need to split
                    diff = np.array(next_pos) - np.array(current_pos)
                    current_pos = next_pos
                    next_pos = (np.array(next_pos) + diff).tolist()
                else:
                    # split the beam horizontally and use recursion
                    beam_starts.append(next_pos)
                    es = trace_beam(
                        arr,
                        current_pos=next_pos,
                        next_pos=(np.array(next_pos) + np.array([0, -1])).tolist(),
                        beam_starts=beam_starts,
                    )
                    energised.extend(es)

                    current_pos = next_pos
                    next_pos = (np.array(next_pos) + np.array([0, 1])).tolist()
            case "|":  # a splitter
                if current_pos[1] == next_pos[1]:
                    # treat this as empty space and no need to split
                    diff = np.array(next_pos) - np.array(current_pos)
                    current_pos = next_pos
                    next_pos = (np.array(next_pos) + diff).tolist()
                else:
                    # split the beam vertically and use recursion
                    beam_starts.append(next_pos)
                    es = trace_beam(
                        arr,
                        current_pos=next_pos,
                        next_pos=(np.array(next_pos) + np.array([-1, 0])).tolist(),
                        beam_starts=beam_starts,
                    )
                    energised.extend(es)

                    current_pos = next_pos
                    next_pos = (np.array(next_pos) + np.array([1, 0])).tolist()
            case _:
                raise ValueError("Unexpected character!")
    return energised


def find_energised_locations(arr: np.ndarray, current_pos: List[int], next_pos: List[int]) -> int:
    """
    Follow all the beams and then count up the number of energised blocks
    :param arr: the map
    :return: number of energised blocks
    """
    a = trace_beam(arr, current_pos, next_pos, [])
    empty = np.zeros_like(arr)
    mask = np.isin(empty, [""])
    empty = np.where(mask, "0", empty)
    for c in a:
        empty[c[0], c[1]] = 1
    return int(np.sum(empty.astype("uint8")))


def find_best_starting_position(arr: np.ndarray) -> int:
    """
    Find the best starting position by positioning the start of the initial beam at every place outside the array
    :param arr: the map
    :return: maximum number of energised squares
    """
    h, w = arr.shape
    # collect all the possible start points
    top_and_down = [([-1, i], [0, i]) for i in range(w)]
    bottom_and_up = [([h, i], [h - 1, i]) for i in range(w)]
    left_to_right = [([i, -1], [i, 0]) for i in range(h)]
    right_to_left = [([i, w], [i, w - 1]) for i in range(h)]
    starting_pos = [*top_and_down, *bottom_and_up, *left_to_right, *right_to_left]
    # iterate over all the possible start points
    ns = [find_energised_locations(arr, s, n) for s, n in starting_pos]
    return max(ns)


def solve(data: List[str], part: str = "a") -> int:
    """
    Solve the problem for day 1
    :param data: input data
    :param part: which part of the problem to solve - 'a' or 'b'
    :return: solution
    """
    arr = np.array([list(line.lstrip()) for line in data])
    if part == "a":
        return find_energised_locations(arr, current_pos=[0, -1], next_pos=[0, 0])
    else:
        return find_best_starting_position(arr)
