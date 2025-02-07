import logging
from itertools import chain
from math import prod
from typing import List

import numpy as np


numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


def calc_distance(x: List[int], y: List[int]) -> int:
    """
    Calculate the maximum distance between two 2D co-ordinates in either dimension

    e.g. given x = [0, 2] and Y= [0, 4] then this function would return 2
    :param x: first co-ordinate
    :param y: second co-ordinate
    :return: maximum distance in either dimension
    """
    return max([abs(x[0] - y[0]), (abs(x[1] - y[1]))])


def encode_data(d: List[str], part: str = "a") -> np.ndarray:
    """
    Encode the list of strings as a numpy array with 3 numeric values

    numbers are encoded as 1
    periods are encoded as 0
    other symbols are encoded as 2 (if part == b then only * is encoded as 2)
    :param d: input data
    :param part: the puzzle part - a or b
    :return: encoded array
    """
    new_d = []
    for s in d:
        for n in numbers:
            s = s.replace(str(n), "1")
        if part == "a":
            s = s.replace(".", "0")
            s_l = list(s)
            s_l = [i if i in ["0", "1"] else "2" for i in s_l]
        else:
            s = s.replace("*", "2")
            s_l = list(s)
            s_l = [i if i in ["1", "2"] else "0" for i in s_l]
        new_d.append(s_l)
    return np.asarray(new_d)


def extract_number_indices(encoded_data: np.ndarray) -> List[List[List[int]]]:
    """
    Extract indices for numbers from the array by finding consecutive 1's in the X dimension
    :param encoded_data: encoded array
    :return: a nested list where each sub list is a list of co-ordinates in the array representing digits of the number
    """
    number_idx: List[List[List[int]]] = []
    idx = np.argwhere(encoded_data == "1").tolist()
    current_no = []
    for i, x in enumerate(idx):
        if x in list(chain(*number_idx)):
            pass
        elif i == len(idx) - 1:
            current_no.append(x)
            number_idx.append(current_no)
            current_no = []
        elif len(current_no) == 0:
            current_no.append(x)
        elif x[1] == current_no[-1][1] + 1:
            current_no.append(x)
        else:
            number_idx.append(current_no)
            current_no = [x]
    return number_idx


def to_array(data: List[str]) -> np.ndarray:
    """
    Convert the input data to an array without encoding
    :param data: input data
    :return: array
    """
    return np.asarray([list(s) for s in data])


def extract_part_numbers(number_idx: List[List[List[int]]], encoded_data: np.ndarray, orig_arr: np.ndarray) -> int:
    """
    Determine which numbers in the array are "parts" numbers

    Given a list of indicies for numbers in the array, determine where the symbols (2's) are in the encoded data,
    iterate over the number indicies and see if any of the symbols are one-step (including diaganols) from the
    number. If so then extract the digits from orig_arr, concatenate to the final number and add to the total
    :param number_idx: positions of numbers in the array
    :param encoded_data: the encoded array
    :param orig_arr: the original array
    :return: the sum of parts numbers
    """
    t = 0
    for numb in number_idx:
        symbols = np.argwhere(encoded_data == "2").tolist()

        valid = any([any([calc_distance(n, s) < 2 for s in symbols]) for n in numb])
        if valid:
            t += int("".join([orig_arr[x[0], x[1]] for x in numb]))
    return t


def find_gears(encoded_data: np.ndarray) -> List[List[int]]:
    """
    Extract the co-ordinates for gears (2's) from the array
    :param encoded_data: the encoded array
    :return: list of co-ordinates for gears
    """
    return np.argwhere(encoded_data == "2").tolist()


def calculate_gear_ratios(encoded_data: np.ndarray, orig_arr: np.ndarray) -> List[int]:
    """
    For each gear, calculate the gear ratio which is the product of its adjacent part numbers
    :param encoded_data: the encoded array
    :param orig_arr: the original data in array form
    :return: list of gear ratios
    """
    gears = find_gears(encoded_data)
    logging.info("Found %s gears!", len(gears))
    numbers_idx = extract_number_indices(encoded_data)
    gear_ratios = []
    for gear in gears:
        adjacency = [any([calc_distance(gear, s) < 2 for s in numb]) for numb in numbers_idx]
        if adjacency.count(True) > 1:
            adjacent_numbers = [numb for i, numb in enumerate(numbers_idx) if adjacency[i]]
            gear_ratio = prod([int("".join([orig_arr[x[0], x[1]] for x in numb])) for numb in adjacent_numbers])
            gear_ratios.append(gear_ratio)
    return gear_ratios


def solve(data: List[str], part: str = "a") -> int:
    """
    Solve the problem for day 3
    :param data: input data
    :param part: which part of the problem to solve - 'a' or 'b'
    :return: solution
    """
    orig_array = to_array(data)
    if part == "a":
        encoded_data = encode_data(data, part)
        number_idx = extract_number_indices(encoded_data)
        total = extract_part_numbers(number_idx, encoded_data, orig_array)
        return total
    else:
        encoded_data = encode_data(data, part)
        ratios = calculate_gear_ratios(encoded_data, orig_array)
        return sum(ratios)
