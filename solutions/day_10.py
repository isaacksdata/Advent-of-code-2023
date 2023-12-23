from itertools import chain
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage
from scipy.ndimage import binary_dilation

symbols = ["|", "L", "J", "F", "-", ".", "Z"]  # 7 replaced with Z to avoid confusion with incrementing path


def numerify(arr: np.ndarray) -> np.ndarray:
    """
    Convert an array of strings to numbers according to the rule: 0 if in symbols, 1 if a number
    :param arr: input array
    :return: numeric array
    """
    mask = np.isin(arr, symbols)
    map_arr = np.where(mask, "0", arr)
    map_arr = map_arr.astype("uint16")  # uint16 to allow for n > 255
    return map_arr


def gen_fig(arr: np.ndarray) -> None:
    """
    Generate an image to show the path from the array map
    :param arr: input array of symbols
    :return: void
    """
    plt.imshow(numerify(arr))


def check_symbol(symbol: str, direction: str, current_idx: str) -> bool:
    """
    Check to see if a symbol found in the map is valid for a given direction
    :param symbol: the entry at the proposed next position
    :param direction: the direction from current position
    :param current_idx: the entry at current position in the maze
    :return: True if the symbol is valid else False
    """
    if symbol == ".":
        return False
    if current_idx == "S":
        if direction == "bottom" and symbol in ["|", "L", "J"]:
            return True
        if direction == "top" and symbol in ["|", "F", "Z"]:
            return True
        if direction == "left" and symbol in ["-", "L", "F"]:
            return True
        if direction == "right" and symbol in ["-", "J", "Z"]:
            return True
        return False

    if current_idx in ["|"]:
        if direction == "bottom" and symbol in ["|", "L", "J"]:
            return True
        if direction == "top" and symbol in ["|", "F", "Z"]:
            return True
        return False
    if current_idx in ["-"]:
        if direction == "left" and symbol in ["-", "L", "F"]:
            return True
        if direction == "right" and symbol in ["-", "J", "Z"]:
            return True
        return False
    if current_idx in ["L"]:
        if direction == "right" and symbol in ["-", "J", "Z"]:
            return True
        if direction == "top" and symbol in ["|", "F", "Z"]:
            return True
        return False
    if current_idx in ["F"]:
        if direction == "right" and symbol in ["-", "J", "Z"]:
            return True
        if direction == "bottom" and symbol in ["|", "L", "J"]:
            return True
        return False
    if current_idx in ["Z"]:
        if direction == "left" and symbol in ["-", "L", "F"]:
            return True
        if direction == "bottom" and symbol in ["|", "L", "J"]:
            return True
    if current_idx in ["J"]:
        if direction == "left" and symbol in ["-", "L", "F"]:
            return True
        if direction == "top" and symbol in ["|", "F", "Z"]:
            return True
        return False
    return False


def get_next_steps(
    arr: np.ndarray, i: str, original_arr: np.ndarray, current_positions: Optional[List[Tuple[int, int]]] = None
) -> List[Tuple[int, int]]:
    """
    Given the current map and current position(s) - find the next possible moves

    If no current _positions are provided - then find the current position using i which is a symbol to search for
    :param arr: the map
    :param i: symbol to search for
    :param original_arr: untouched original array with symbols - used for extracting previous positions
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
                if check_symbol(arr[c], direction, original_arr[idx[0], idx[1]]):
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


def take_steps(
    arr: np.ndarray, steps: Dict[int, List[Tuple[int, int]]], i: int, step_history: Dict[int, List[Tuple[int, int]]]
) -> Tuple[np.ndarray, Dict[int, List[Tuple[int, int]]]]:
    """
    Given a dictionary of steps along each side of the loop - take the next possible steps

    This means replacing the next positions in the map with i which is np.max(arr) + 1
    :param arr: current map
    :param steps: a dict of next steps
    :param i: step number
    :param step_history: a dictionary mapping all previous steps along each side of the loop. Each step is a tuple.
    :return: updated map, step_history
    """
    for loop, s in steps.items():
        step_history[loop].extend(s)
    for step in list(chain(*list(steps.values()))):
        arr[step] = i
    return arr, step_history


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


def find_path(arr: np.ndarray) -> Tuple[np.ndarray, int, Dict[int, List[Tuple[int, int]]]]:
    """
    Find the looping path through the array and stop at the point where the two sides of the loop meet
    :param arr: input map
    :return: mapped array, number of steps to meeting point, step_history
    """
    i = 0  # step counter
    start = np.where(arr == "S")
    original_arr = arr.copy()
    arr[start] = 0
    steps = get_next_steps(arr, str(i), original_arr)
    steps_dict = {0: [steps[0]], 1: [steps[1]]}
    step_history: Dict[int, List[Tuple[int, int]]] = {0: [], 1: []}
    while not check_steps_for_end(arr, steps_dict):
        i += 1
        arr, step_history = take_steps(arr, steps_dict, i, step_history)
        for key, pos in steps_dict.items():
            steps_dict[key] = get_next_steps(arr, str(i), original_arr, pos)
        if any([v == [] for v in steps_dict.values()]):
            raise ValueError()
    arr, step_history = take_steps(arr, steps_dict, i + 1, step_history)
    return arr, i + 1, step_history


def find_steps(data: List[str]) -> Tuple[int, np.ndarray, Dict[int, List[Tuple[int, int]]]]:
    """
    Find the number of steps taken to reach the middle of the loop
    :param data: input data
    :return: num of steps, mapped array with path and mapping of steps
    """
    arr = np.array([list(l.replace("7", "Z")) for l in data])
    arr = arr.astype("<U5")  # allows strings upto 5 digits long in the array
    mapped_arr, i, step_history = find_path(arr)
    return i, mapped_arr, step_history


def find_n_steps(data: List[str]) -> int:
    """
    Find the number of steps taken to reach middle of loop
    :param data: input data
    :return: number of steps required
    """
    n, _, _ = find_steps(data)
    return n


def remove_connected_to_edge(binary_image: np.ndarray) -> np.ndarray:
    """
    Remove connected components which touch the edge of the array
    :param binary_image: input binary image of 0s and 1s
    :return: image without any components which touch the edge
    """
    # Label connected components
    labeled_image, num_labels = ndimage.label(binary_image, structure=[[1, 1, 1], [1, 1, 1], [1, 1, 1]])

    # Find pixels connected to the edge
    edge_labels = np.unique(
        np.concatenate(
            (
                labeled_image[0, :],
                labeled_image[-1, :],
                labeled_image[:, 0],
                labeled_image[:, -1],
            )
        )
    )

    # Remove pixels connected to the edge
    binary_image[np.isin(labeled_image, edge_labels)] = 0

    return binary_image


def make_maze_quick(arr: np.ndarray, step_history: Dict[int, List[Tuple[int, int]]]) -> np.ndarray:
    """
    Convert the path from input arr to a 3x bigger array

    In the original array, one entry represents the path and the walls.
    In the 3x array, the walls and the path and represented by separate entries
    :param arr: input array
    :param step_history: history of steps taken to solve the maze
    :return: 3x array
    """
    big_arr = np.zeros([arr.shape[0] * 3, arr.shape[1] * 3])
    coords = [*step_history[0], *list(reversed(step_history[1]))]
    if not len(arr.shape) == 2:
        raise ValueError("Numpy array should be 2-dimensional!")
    # we have checked above to make sure the np.argwhere() results will be tuples of len 2
    start: Tuple[int, int] = tuple(int(i) for i in np.argwhere(arr == "0").squeeze().tolist())  # type: ignore
    coords.insert(0, start)
    coords.append(start)
    for i, c in enumerate(coords):
        try:
            cn = coords[i + 1]
        except IndexError:
            break
        else:
            min_y = min(c[0] * 3, cn[0] * 3)
            max_y = max(c[0] * 3, cn[0] * 3)
            max_y = max_y + 1 if max_y == min_y else max_y
            min_x = min(c[1] * 3, cn[1] * 3)
            max_x = max(c[1] * 3, cn[1] * 3)
            max_x = max_x + 1 if max_x == max_x else max_x
            big_arr[min_y:max_y, min_x:max_x] = 1
    return big_arr


def count_interior(arr: np.ndarray) -> np.ndarray:
    """
    Isolate the array entries (pixels) which are enclosed within the maze but are not part of the path
    :param arr: 3x size maze - output of make_maze_quick()
    :return: array of enclosed pixels
    """
    structure_element = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    dilated_maze = binary_dilation(arr, structure=structure_element)
    outside_mask = np.logical_not(ndimage.binary_fill_holes(arr).astype(int))
    inverted_array = np.logical_not(dilated_maze)
    inverted_array[outside_mask == 1] = 0
    cleaned_array = remove_connected_to_edge(inverted_array)
    return cleaned_array


def solve(data: List[str], part: str = "a", return_array: bool = False) -> int:
    """
    Solve the problem for day 1
    :param data: input data
    :param part: which part of the problem to solve - 'a' or 'b'
    :return: solution
    """
    if part == "a":
        return find_n_steps(data)
    else:
        _, map_arr, step_history = find_steps(data)
        maze = make_maze_quick(map_arr, step_history)
        final_arr = count_interior(maze)
        return np.sum(final_arr) / 9


# if __name__ == "__main__":
#     test_data = [
#         "...........",
#         ".S-------7.",
#         ".|F-----7|.",
#         ".||.....||.",
#         ".||.....||.",
#         ".|L-7.F-J|.",
#         ".|..|.|..|.",
#         ".L--J.L--J.",
#         "...........",
#     ]
#     # test_data = [
#     #     ".F----7F7F7F7F-7....",
#     #     ".|F--7||||||||FJ....",
#     #     ".||.FJ||||||||L7....",
#     #     "FJL7L7LJLJ||LJ.L-7..",
#     #     "L--J.L7...LJS7F-7L7.",
#     #     "....F-J..F7FJ|L7L7L7",
#     #     "....L7.F7||L7|.L7L7|",
#     #     ".....|FJLJ|FJ|F7|.LJ",
#     #     "....FJL-7.||.||||...",
#     #     "....L---J.LJ.LJLJ..."
#     # ]
#     test_data = [
#         "FF7FSF7F7F7F7F7F---7",
#         "L|LJ||||||||||||F--J",
#         "FL-7LJLJ||||||LJL-77",
#         "F--JF--7||LJLJ7F7FJ-",
#         "L---JF-JLJ.||-FJLJJ7",
#         "|F|F-JF---7F7-L7L|7|",
#         "|FFJF7L7F-JF7|JL---7",
#         "7-L-JL7||F7|L7F-7F7|",
#         "L.L7LFJ|||||FJL7||LJ",
#         "L7JLJL-JLJLJL--JLJ.L",
#     ]
#
#     # from solutions.utilities import (
#     #     get_puzzle,
#     #     submit_answer,
#     #     save_sample_data,
#     #     format_input_data,
#     # )
#     # data = get_puzzle(year=2023, day=10)
#     # test_data = format_input_data(data)
#     _, map_arr, step_history = solve(test_data, "a", True)
#     # binarise(map_arr)
#     maze = make_maze_quick(map_arr, step_history)
#     final_arr = count_interior(maze)
#     print(np.sum(final_arr) / 9)
