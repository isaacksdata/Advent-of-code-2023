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
    if np.all([x >= 0 for x in current_pos]):
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


def find_energised_locations(arr: np.ndarray) -> int:
    """
    Follow all the beams and then count up the number of energised blocks
    :param arr: the map
    :return: number of energised blocks
    """
    a = trace_beam(arr, [0, -1], [0, 0], [])
    empty = np.zeros_like(arr)
    mask = np.isin(empty, [""])
    empty = np.where(mask, "0", empty)
    for c in a:
        empty[c[0], c[1]] = 1
    return int(np.sum(empty.astype("uint8")))


def solve(data: List[str], part: str = "a") -> int:
    """
    Solve the problem for day 1
    :param data: input data
    :param part: which part of the problem to solve - 'a' or 'b'
    :return: solution
    """
    if part == "a":
        arr = np.array([list(line.lstrip()) for line in data])
        return find_energised_locations(arr)
    else:
        return 1


# if __name__ == "__main__":
# pattern = r"""
# .|...\....
# |.-.\.....
# .....|-...
# ........|.
# ..........
# .........\
# ..../.\\..
# .-.-/..|..
# .|....-|.\
# ..//.|....
# """
#
# # Split the pattern into lines
# lines = pattern.strip().split("\n")
#
# # Create a numpy array from the lines
# array = np.array([list(line.lstrip()) for line in lines])
#
# a = find_energised_locations(array)

# from solutions.utilities import (
#     get_puzzle,
#     submit_answer,
#     save_sample_data,
#     format_input_data,
#     run_and_measure,
# )
# data = get_puzzle(year=2023, day=16)
# data = format_input_data(data)
# solve(data, "a")
