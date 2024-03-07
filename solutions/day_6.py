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


def generate_ranges(big_number: int, step: int, start: int = 0) -> List[Tuple[int, int]]:
    """
    Split a big number up into a list of ranges which cover the range of 0 to big number

    Example:
    The number 100 could be represented as a list of ranges each of step 10

    :param big_number: the number to split up
    :param step: the step size to use for ranges
    :param start: the starting number to use
    :return: list of ranges
    """
    ranges = []

    for s in range(start, big_number, step):
        end = min(s + step, big_number)
        ranges.append((s, end))

    return ranges


def test_range(r: Tuple[int, int], d: int, step: int, max_time: int) -> int:
    """
    Test to see if a range beats the distance d

    It is safe to assume that if the start of the range and the end of the range have the same result then all
    values between will have the same result
    :param r: input range (start, finish)
    :param d: the distance to beat
    :param step: the step size
    :param max_time: the max time allowed
    :return: number of strategies which beat d
    """
    lower = get_distance(r[0], max_time - r[0]) > d
    upper = get_distance(r[1], max_time - r[1]) > d
    if lower and upper:
        return step
    if not lower and not upper:
        return 0
    return sum([get_distance(t, max_time - t) > d for t in range(r[0], r[1])])


def solve_big_race(max_time: int, record_distance: int, step: int, start: int = 1) -> int:
    """
    Solution for part b - the big race where it is inefficient to try every possible strategy

    Instead split the time limit into buckets and only do a detailed check on buckets where the bottom and top of the
    range do not give the same answer
    :param max_time: time limit for the race
    :param record_distance: distance to beat
    :param step: step size for buckets
    :param start: starting value to use
    :return: number of winning strategies
    """
    buckets = generate_ranges(max_time, step, start)
    ns = [test_range(r, record_distance, step, max_time) for r in buckets]
    return sum(ns)


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
        max_time = int("".join(map(str, get_times(data))))
        max_distance = int("".join(map(str, get_distances(data))))
        return solve_big_race(max_time=max_time, record_distance=max_distance, step=1000)
