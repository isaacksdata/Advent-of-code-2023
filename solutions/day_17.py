from queue import PriorityQueue
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Self
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np


direction_mapping: Dict[Tuple[int, int], str] = {(0, 1): "right", (0, -1): "left", (1, 0): "down", (-1, 0): "up"}


def get_possible_moves(
    pos: List[int],
    shape: Tuple[int, ...],
    latest_moves: List[str],
    n_latest_direction: int,
    max_consecutive: int,
    min_turning: int,
) -> List[Tuple[List[int], str]]:
    """
    Determine what moves are possible based on current position and most recent moves
    :param pos: current coordinates e.g. [2, 3]
    :param shape: shape of the whole array
    :param latest_moves: list of latest moves e.g. ["up", "left", "left"]
    :param n_latest_direction: number of moves in current direction
    :param max_consecutive : maximum consecutive moves that can be made in one direction
    :param min_turning: minimum number of moves which must be made in one direction before turning
    :return: a list of possible moves
    """
    moves = []
    n_moves = len(latest_moves)
    if n_moves < min_turning or n_latest_direction < min_turning:
        if n_moves == 0:
            moves.append(([pos[0], pos[1] + 1], "right"))
            moves.append(([pos[0] + 1, pos[1]], "down"))
            return moves
        lm = latest_moves[-1]
        move = [k for k, v in direction_mapping.items() if v == lm][0]
        if (
            (pos[1] > 0 and lm == "left")
            or ((pos[1] < shape[1] - 1 and lm == "right") or (pos[0] > 0 and lm == "up"))
            or (pos[0] < shape[0] - 1 and lm == "down")
        ):
            moves.append(((np.array(pos) + np.array(move)).tolist(), lm))
        return moves
    l = latest_moves[-1] if n_moves > 0 else ""
    # can move left?
    if pos[1] > 0 and (n_moves < max_consecutive or not np.all([m == "left" for m in latest_moves])) and l != "right":
        moves.append(([pos[0], pos[1] - 1], "left"))
    # can move right?
    if (
        pos[1] < shape[1] - 1
        and (n_moves < max_consecutive or not np.all([m == "right" for m in latest_moves]))
        and l != "left"
    ):
        moves.append(([pos[0], pos[1] + 1], "right"))
    # can move up?
    if pos[0] > 0 and (n_moves < max_consecutive or not np.all([m == "up" for m in latest_moves])) and l != "down":
        moves.append(([pos[0] - 1, pos[1]], "up"))
    # can move down?
    if (
        pos[0] < shape[0] - 1
        and (n_moves < max_consecutive or not np.all([m == "down" for m in latest_moves]))
        and l != "up"
    ):
        moves.append(([pos[0] + 1, pos[1]], "down"))
    return moves


class Pointer:
    """
    A class to represent the current position
    """

    def __init__(self, pos: List[int], directions: List[str], total: int, max_consecutive: int = 3) -> None:
        self._pos: List[int] = pos
        self._directions: List[str] = directions
        self.total: int = total
        self.max_consecutive: int = max_consecutive

    def update_position(self, pos: List[int]) -> None:
        """
        Update the current position
        :param pos: co-ordinates of current position
        :return: void
        """
        self._pos = pos

    def add_direction(self, d: str) -> None:
        """
        Add the new direction to the stored list of directions

        Only need to store latest 3 directions
        :param d: new direction
        :return: void
        """
        if len(self._directions) == self.max_consecutive:
            _ = self._directions.pop(0)
        self._directions.append(d)

    def update_total(self, n: int) -> None:
        """
        Update the total cost
        :param n: cost to add to total cost
        :return: void
        """
        self.total += n

    def __gt__(self, other: int) -> bool:
        """
        Check if self._total is greater than the supplied value
        :param other: other value
        :return: True if self._total is greater
        """
        return self.total > other

    def __lt__(self, other: int) -> bool:
        """
        Check if self._total is smaller than the supplied value
        :param other: other value
        :return: True if self._total is smaller
        """
        return self.total < other

    def get_state(self) -> Tuple[Optional[str], int]:
        """
        Get the most recent direction and how many times have moved consecutively in that direction
        :return: the direction and count of that direction
        """
        d = self._directions[-1] if self._directions else None
        if d is None:
            count = 0
        else:
            count = 0
            for i in reversed(self._directions):
                if i == d:
                    count += 1
                else:
                    break
        return d, count

    @property
    def pos(self) -> Tuple[int, ...]:
        """
        Get the co-ordinates of the position
        :return: position
        """
        return tuple(self._pos)

    @property
    def directions(self) -> List[str]:
        return self._directions

    def __copy__(self, pos: Optional[List[int]] = None) -> Self:
        """
        Create a new instance and copy the relevant attributes
        :param pos: the new position
        :return: new instance of Pointer
        """
        pos = self._pos if pos is None else pos
        new_instance = self.__class__(
            pos=pos, directions=self._directions.copy(), total=self.total, max_consecutive=self.max_consecutive
        )
        return new_instance


def heuristic(a: List[int], b: Tuple[int, ...]) -> int:
    """
    Manhattan distance on a square grid between two points
    :param a: point one
    :param b: point two
    :return: distance
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def find_path(arr: np.ndarray, pos: List[int], total: int = 0, max_consecutive: int = 3, min_turning: int = 0) -> int:
    """
    Find the lowest cost path from pos to bottom right corner of the array
    :param arr: input array with costs as entries
    :param pos: the starting position
    :param total: the starting total cost
    :param max_consecutive: maximum number of steps that can be taken in one direction
    :param min_turning: minimum number of steps in one direction before turning or finishing
    :return: the smallest cost incurred whilst getting to end
    """
    frontier: PriorityQueue = PriorityQueue()
    starter = Pointer(pos=pos, directions=[], total=total, max_consecutive=max_consecutive)
    frontier.put((0, starter))
    came_from: Dict[Tuple[Tuple[int, ...], Optional[str], int], Any] = {(tuple(pos), "", 0): None}
    cost_so_far: Dict[Tuple[Tuple[int, ...], Optional[str], int], int] = {(tuple(pos), "", 0): 0}

    end = [i - 1 for i in arr.shape]  # bottom right corner

    end_state: Optional[Tuple[Tuple[int, ...], Optional[str], int]] = None

    while not frontier.empty():
        _, p = frontier.get()
        if p.pos == tuple(end) and p.get_state()[1] >= min_turning:
            d, n = p.get_state()
            end_state = (p.pos, d, n)
            break
        possible_moves = get_possible_moves(
            p.pos, arr.shape, p.directions, p.get_state()[1], max_consecutive, min_turning
        )
        for pm in possible_moves:
            p_next: Pointer = p.__copy__(pos=pm[0])
            p_next.update_total(arr[pm[0][0], pm[0][1]])
            p_next.add_direction(d=pm[1])
            if (p_next.pos, *p_next.get_state()) not in cost_so_far or p_next < cost_so_far[
                (p_next.pos, *p_next.get_state())
            ]:
                cost_so_far[(p_next.pos, *p_next.get_state())] = p_next.total
                priority = p_next.total + heuristic(end, p_next.pos)
                frontier.put((priority, p_next))
                came_from[(p_next.pos, *p_next.get_state())] = (p.pos, *p.get_state())

    if end_state is None:
        raise ValueError("Did not reach the goal!")
    best_path = []
    start = tuple(pos)
    current = end_state
    while current[0] != start:
        if came_from[current][0] != start:
            best_path.append(came_from[current])
        current = came_from[current]
    best_path.insert(0, (tuple(end), ()))
    total_cost = 0
    empty = np.zeros_like(arr).astype("uint8")
    for i in best_path:
        i = i[0]
        empty[i[0], i[1]] = 1
        total_cost += arr[i[0], i[1]]
    return total_cost


def solve(data: List[str], part: str = "a") -> int:
    """
    Solve the problem for day 1
    :param data: input data
    :param part: which part of the problem to solve - 'a' or 'b'
    :return: solution
    """
    arr = np.array([list(map(int, list(l))) for l in data])
    if part == "a":
        return find_path(arr, [0, 0])
    else:
        return find_path(arr, [0, 0], max_consecutive=10, min_turning=4)
