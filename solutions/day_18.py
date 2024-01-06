from dataclasses import dataclass
from typing import Dict
from typing import List
from typing import Tuple
from typing import Union

import numpy as np
from scipy import ndimage


HEXA_DIR_MAP: Dict[int, str] = {0: "R", 1: "D", 2: "L", 3: "U"}


@dataclass
class Instruction:
    """
    A simple dataclass for storing each instruction in the input dataset
    """

    direction: str
    length_str: str
    color: str
    part: str

    def __post_init__(self) -> None:
        # Convert length_str to an integer during post-init
        if self.part == "a":
            self.length = int(self.length_str)
        else:
            self.length = int(self.color[2:-2], 16)
            d = self.color[-2]
            self.direction = HEXA_DIR_MAP[int(d)]


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


def get_next_position(current_pos: List[int], i: Instruction) -> List[int]:
    """
    Given current position and instructions i, determine the position after the instruction has been executed
    :param current_pos: current position before instruction
    :param i: the instruction to carry out
    :return: the position after instruction
    """
    if i.direction == "R":
        next_pos = [current_pos[0], current_pos[1] + int(i.length)]
    if i.direction == "L":
        next_pos = [current_pos[0], current_pos[1] - int(i.length)]
    if i.direction == "U":
        next_pos = [current_pos[0] - int(i.length), current_pos[1]]
    if i.direction == "D":
        next_pos = [current_pos[0] + int(i.length), current_pos[1]]
    return next_pos


def get_instructions(data: List[str]) -> List[Instruction]:
    """
    Convert the input data to a list of Instruction dataclass instances
    :param data: input data
    :return: List of instructions
    """
    return [Instruction(direction=d[0], length_str=d[1], color=d[2], part="a") for d in (d.split(" ") for d in data)]


def create_map(data: List[str]) -> np.ndarray:
    """
    Create a map from the instructions

    The instructions indicate where the edge of the lagoon should be dug - by drawing this onto the map we create a
    perimeter. Ndimage is then used to fill the perimeter so we can calculate the total area.
    :param data: input data
    :return: completed map
    """
    instructions = get_instructions(data)

    xmin, xmax, ymin, ymax = get_limits(instructions=instructions)
    arr = np.zeros([(xmax - xmin) + 10, (ymax - ymin) + 10])

    current_pos = [abs(xmin) + 5, abs(ymin) + 5]
    for i in instructions:
        next_pos = get_next_position(current_pos, i)
        row1, col1 = current_pos
        row2, col2 = next_pos

        # Set all pixels between the two coordinates (inclusive) to 1
        arr[min(row1, row2) : max(row1, row2) + 1, min(col1, col2) : max(col1, col2) + 1] = 1

        current_pos = next_pos
    filled_arr = ndimage.binary_fill_holes(arr).astype(int)
    return filled_arr


def shoelace_theorem(vertices: List[List[int]]) -> float:
    """
    Use the Shoelace Theorem to calculate the area of a polygon using its vertices.

    The area (A) of a polygon with vertices (x1, y1), (x2, y2), ..., (xn, yn) is given by:

    A = 0.5 * |x1y2 + x2y3 + ... + xn*y1 - x2y1 - x3y2 - ... - x1yn|

    This formula pairs consecutive vertices and sums the products of their coordinates,
    then calculates the absolute difference between the two accumulated sums and divides
    by 2 to obtain the area of the polygon.
    :param vertices: the known vertices of the polygon
    :return: the area of the polygon
    """
    n = len(vertices)
    area = 0.0

    for i in range(n - 1):
        area += vertices[i][0] * vertices[i + 1][1]
        area -= vertices[i + 1][0] * vertices[i][1]

    # Add the contribution of the last edge
    area += vertices[n - 1][0] * vertices[0][1]
    area -= vertices[0][0] * vertices[n - 1][1]

    # Take the absolute value and divide by 2
    area = abs(area) / 2.0

    return area


def picks_theorem(b: int, area: Union[float, int]) -> int:
    """
    This function determines the number of interior lattice points from the number of boundary points
    and the area of the polygon.

    A = I + B/2 - 1
    where A is the area of the polygon, B is the number of boundary points and I is the number of interior lattice
    points
    :param b: number of boundary points
    :param area: area of the polygon
    :return: number of interior lattice points
    """
    return int(area + 1 - (b / 2))


def get_vertices(instructions: List[Instruction]) -> List[List[int]]:
    """
    Get a list of vertices for the polygon described by the instructions
    :param instructions: list of directions and distances in each direction
    :return: List of co-ordinates for vertices
    """
    xmin, xmax, ymin, ymax = get_limits(instructions=instructions)
    current_pos = [abs(xmin) + 5, abs(ymin) + 5]
    vertices = [current_pos]
    for i in instructions:
        next_pos = get_next_position(current_pos, i)
        vertices.append(next_pos)
        current_pos = next_pos
    return vertices


def get_big_area(data: List[str]) -> int:
    """
    Get the area of the lagoon for Part B

    The distances involved this time are huge so it is not feasible to create an array. Instead, track the vertices
    and then use the Shoelace theorem to calculate the area of the polygon. Then we use Picks Theorem to find the
    number of discrete cube units within the polygon. Then add back on the border length of the polygon.
    :param data: input data
    :return: total area
    """
    instructions = get_instructions(data)
    vertices = get_vertices(instructions)
    total_distance = int(np.sum([i.length for i in instructions]))
    return picks_theorem(b=total_distance, area=shoelace_theorem(vertices)) + total_distance


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
        return get_big_area(data)
