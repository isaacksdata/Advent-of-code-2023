import math
from typing import List
from typing import Tuple


def get_times(data: List[str]) -> List[int]:
    """
    Extract time limits for each race
    :param data: input data
    :return: list of time limits
    """
    return list(map(int, data[0].split(": ")[1].split()))


def get_distances(data: List[str]) -> List[int]:
    """
    Extract record distances for each race
    :param data: input data
    :return: list of distances
    """
    return list(map(int, data[1].split(": ")[1].split()))


def get_distance(speed: int, time: int) -> int:
    """
    Calculate distance from speed and time
    :param speed: boat speed
    :param time: time for travel
    :return: distance travelled
    """
    return speed * time


def find_strategies(max_time: int) -> List[Tuple[int, int]]:
    """
    Find all strategies for a given race

    A strategy consists of how much time spent holding the button and how much time moving
    This functions returns a list of tuples where each tuple is a strategy. The first entry to the tuple is the
    time spent holding the button (equates to speed) and the second element is the time left for moving
    :param max_time: time limit of the race
    :return: possible strategies
    """
    return [(i, max_time - i) for i in range(1, max_time)]


def find_winnning_strategies(max_time: int, record_distance: int) -> int:
    """
    Collect possible strategies and determine which ones would beat the record distance. Return number of winning
    strategies
    :param max_time: time limit for the race
    :param record_distance: distance to beat
    :return: number of winning strategies
    """
    strategies = find_strategies(max_time)
    distances = [get_distance(*s) for s in strategies]
    return [d > record_distance for d in distances].count(True)


def solve(data: List[str], part: str = "a") -> int:
    """
    Solve the problem for day 1
    :param data: input data
    :param part: which part of the problem to solve - 'a' or 'b'
    :return: solution
    """
    if part == "a":
        times = get_times(data)
        distances = get_distances(data)
        return math.prod([find_winnning_strategies(t, d) for t, d in zip(times, distances)])
    else:
        return 1
