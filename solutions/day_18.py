from dataclasses import dataclass
from typing import List
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage


@dataclass
class Instruction:
    """
    A simple dataclass for storing each instruction in the input dataset
    """

    direction: str
    length_str: str
    color: str

    def __post_init__(self) -> None:
        # Convert length_str to an integer during post-init
        self.length = int(self.length_str)


def get_limits(instructions: List[Instruction]) -> Tuple[int, ...]:
    """
    From the list of instructions, calculate the limits of travel so an appropriately sized array can be initiated

    Note that the instructions may lead to xmin and ymin being negative
    :param instructions: list of instructions for direction and length
    :return: min_x, max_x, min_y, max_y
    """
    max_x, min_x, max_y, min_y = 0, 0, 0, 0
    current_x, current_y = 0, 0
    for i in instructions:
        if i.direction == "U":
            current_x -= int(i.length)
        if i.direction == "D":
            current_x += int(i.length)
        if i.direction == "R":
            current_y += int(i.length)
        if i.direction == "L":
            current_y -= int(i.length)
        if current_y > max_y:
            max_y = current_y
        if current_x > max_x:
            max_x = current_x
        if current_x < min_x:
            min_x = current_x
        if current_y < min_y:
            min_y = current_y
    return min_x, max_x, min_y, max_y


def create_map(data: List[str]) -> np.ndarray:
    """
    Create a map from the instructions

    The instructions indicate where the edge of the lagoon should be dug - by drawing this onto the map we create a
    perimeter. Ndimage is then used to fill the perimeter so we can calculate the total area.
    :param data: input data
    :return: completed map
    """
    instructions = [Instruction(*d.split(" ")) for d in data]
    xmin, xmax, ymin, ymax = get_limits(instructions=instructions)
    arr = np.zeros([(xmax - xmin) + 10, (ymax - ymin) + 10])

    current_pos = [abs(xmin) + 5, abs(ymin) + 5]
    next_pos = current_pos
    for i in instructions:
        if i.direction == "R":
            next_pos = [current_pos[0], current_pos[1] + int(i.length)]
        if i.direction == "L":
            next_pos = [current_pos[0], current_pos[1] - int(i.length)]
        if i.direction == "U":
            next_pos = [current_pos[0] - int(i.length), current_pos[1]]
        if i.direction == "D":
            next_pos = [current_pos[0] + int(i.length), current_pos[1]]
        row1, col1 = current_pos
        row2, col2 = next_pos

        # Set all pixels between the two coordinates (inclusive) to 1
        arr[min(row1, row2) : max(row1, row2) + 1, min(col1, col2) : max(col1, col2) + 1] = 1

        current_pos = next_pos
    filled_arr = ndimage.binary_fill_holes(arr).astype(int)
    return filled_arr


def solve(data: List[str], part: str = "a") -> int:
    """
    Solve the problem for day 1
    :param data: input data
    :param part: which part of the problem to solve - 'a' or 'b'
    :return: solution
    """
    if part == "a":
        return int(np.sum(create_map(data)))
    else:
        return 1


# if __name__ == "__main__":
#     from solutions.utilities import (
#         get_puzzle,
#         submit_answer,
#         save_sample_data,
#         format_input_data,
#         run_and_measure,
#     )
#
#     data = get_puzzle(year=2023, day=18)
#     data = format_input_data(data)
#     solve(data)
