import itertools
from collections import deque
from typing import Deque
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

import tqdm


def map_value(value: int, dest_start: int, source_start: int, range: int) -> Optional[int]:
    """
    Map the provided value from the source space to the destination space

    If the value does not lie within the provided ranges then None is returned
    :param value: input value from source space
    :param dest_start: the start of the destination space
    :param source_start: the start of the source space
    :param range: the range of the source and destination spaces
    :return: mapped value
    """
    if source_start <= value <= source_start + range:
        return dest_start + (value - source_start)
    return None


def clean_input(data: List[str]) -> Tuple[List[int], List[str]]:
    """
    Clean up the input data for easier processing
    :param data: input data
    :return: cleand data
    """
    data = [x for x in data if x != ""]
    seeds = data[0]
    seed_ids = list(map(int, seeds.split(":")[1].split()))
    data = data[1:]
    return seed_ids, data


def create_maps(data: List[str]) -> Dict[str, List[str]]:
    """
    Create a dictionary of maps to be used for mapping between spaces
    :param data: input data
    :return: a dictionary of mappings for each space transformation
    """
    maps: Dict[str, List[str]] = {}
    current_map = ""
    for i in data:
        if "map" in i:
            current_map = i
            maps[current_map] = []
        else:
            maps[current_map].append(i)
    return maps


def map_seed(seed: int, maps: Dict[str, List[str]]) -> int:
    """
    Map seed to location by iterating over the transformations stored within maps
    :param seed: the seed ID
    :param maps: the dictionary of mappings
    :return: the seed location
    """
    current_value = seed
    for m, mappings in maps.items():
        mapped_value = None
        for mapping in mappings:
            mapping_vals = list(map(int, mapping.split()))
            mapped_value = map_value(current_value, *mapping_vals)
            if mapped_value is not None:
                break
        if mapped_value is not None:
            current_value = mapped_value
    return current_value


def ranges_overlap(range1: List[int], range2: List[int]) -> bool:
    """
    Check if there is any overlap between the two number specified number ranged
    :param range1: a range of numbers described by start:end
    :param range2: a range of numbers described by start:end
    :return: True if the ranges overlap
    """
    overlap = not (range1[1] < range2[0] or range2[1] < range1[0])
    return overlap


def map_range(r: List[int], m: List[int]) -> Tuple[Tuple[int, int] | Tuple, List[List[int]]]:
    """
    Map a number range r to a new space using a mapping m. Unmappable ranges are returned as the remainder

    Mapping m is a list of three numbers as follows:
    Entry 0: start of the destination space
    Entry 1: start of the source space
    Entry 2: length of the source and destination spaces

    If the ranges do not overlap then an empty tuple is returned for mapped space and the original source space is
    returned as the remainder

    Example:
    let r=[10, 20] and m = [30, 5, 10]
    The range of numbers 10->20 is partially covered by the source space 5->14
    Numbers 10->14 can be mapped to the destination space and become 35->39
    Numbers 15->20 cannot be mapped using this mapping and so would be returned as a remainder
    For this example, the function would return (35, 39), [[15, 20]]

    :param r: input space e.g. [10, 20]
    :param m: input mapping e.g. [30, 5, 10]
    :return: the mapped range, the remainder ranges
    """
    buckets = []
    if not ranges_overlap(r, [m[1], m[1] + m[2] - 1]):
        return (), [r]
    if r[0] < m[1]:
        lower_remainder = [r[0], m[1] - 1]
        mappable_l = m[1]
        buckets.append(lower_remainder)
    else:
        mappable_l = r[0]
    if r[1] > m[1] + m[2] - 1:
        upper_remainder = [m[1] + m[2], r[1]]
        mappable_h = m[1] + m[2] - 1
        buckets.append(upper_remainder)
    else:
        mappable_h = r[1]
    mappable_range = (map_value(mappable_l, *m), map_value(mappable_h, *m))
    if None in mappable_range:
        raise ValueError("Should not get None in the mapped range here")
    return mappable_range, buckets


def map_seed_b(seed_low: int, seed_high: int, maps: Dict[str, List[str]]) -> int:
    """
    Map seed range to locations by iterating over the transformations stored within maps

    :param seed_low: the seed ID range lower bound
    :param seed_high: the seed ID range upper bound
    :param maps: the dictionary of mappings
    :return: the lowest seed location
    """
    ranges: List[Tuple[int, int] | Tuple] = [(seed_low, seed_high)]
    for m_name, mappings in maps.items():
        formatted_mappings = [list(map(int, m.split())) for m in mappings]
        remainders: Deque = deque()
        remainders.extend(ranges)
        new_ranges = []
        while len(remainders) > 0:
            r = remainders.popleft()
            did_map = False
            for m in formatted_mappings:
                mapped, rms = map_range(r, m)
                if len(mapped) > 0 and len(rms) == 0:  # all mapped
                    new_ranges.append(mapped)
                    did_map = True
                    break
                if len(mapped) > 0 and len(rms) > 0:  # partial mapped
                    new_ranges.append(mapped)
                    remainders.extend(rms)
                    did_map = True
                    break
            if not did_map:
                remainders.append(r)
            if not any(
                ranges_overlap(r, [m[1], m[2] + m[1] - 1]) for r, m in itertools.product(remainders, formatted_mappings)
            ):
                new_ranges.extend(remainders)
                remainders.clear()
                break
            formatted_mappings.reverse()
        ranges = new_ranges

    min_vals = [min(r) for r in ranges]
    return min(min_vals)


def get_closest_location(data: List[str]) -> int:
    """
    Across the seeds, find the one with the smallest location value
    :param data: input data
    :return: smallest location
    """
    seeds, clean_data = clean_input(data)
    maps = create_maps(clean_data)
    locations = []
    for seed in tqdm.tqdm(seeds):
        l = map_seed(seed, maps)
        locations.append(l)
    return min(locations)


def get_closest_location_b(data: List[str]) -> int:
    """
    Across the seeds, find the one with the smallest location value
    :param data: input data
    :return: smallest location
    """
    seeds, clean_data = clean_input(data)
    seed_groups = [(x, seeds[i + 1]) for i, x in enumerate(seeds) if i % 2 == 0]
    maps = create_maps(clean_data)
    locations = []
    for seed_l, r in tqdm.tqdm(seed_groups):
        l = map_seed_b(seed_l, seed_l + r, maps)
        locations.append(l)
    return min(locations)


def solve(data: List[str], part: str = "a") -> int:
    """
    Solve the problem for day 1
    :param data: input data
    :param part: which part of the problem to solve - 'a' or 'b'
    :return: solution
    """
    if part == "a":
        return get_closest_location(data)
    else:
        return get_closest_location_b(data)
