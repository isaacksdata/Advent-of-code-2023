from typing import Dict
from typing import List


def get_hash(s: str) -> int:
    """
    Get the HASH for a provided string

    ord() is used to get the ascii value for a particular character
    :param s: input string
    :return: hash value
    """
    v = 0
    for x in list(s):
        ascii_val = ord(x)
        v += ascii_val
        v *= 17
        v = v % 256
    return v


def organise_lenses(operations: List[str]) -> Dict[int, List[str]]:
    """
    Organise the boxes of lens according to the list of instructions

    Instructions with "-" mean to remove a lens from a box
    e.g. rn- means remove lens with the label "rn" from box get_hash("rn")

    Instructions with "=" mean to replace or add a lens to a box
    e.g. ab=8 means add the lens with label "ab" and focal length 9 to box get_hash("ab")

    :param operations: list of instructions
    :return: dictionary of organised lens boxes
    """
    boxes: Dict[int, List[str]] = {}
    for op in operations:
        if "=" in op:
            label, fl = op.split("=")
            f = "="
        else:
            label = op.split("-")[0]
            fl = None
            f = "-"
        hashmap = get_hash(label)
        if hashmap not in boxes:
            boxes[hashmap] = []
        if f == "=":
            try:
                i = [i for i, x in enumerate(boxes[hashmap]) if x.split()[0] == label][0]
            except IndexError:
                boxes[hashmap].append(f"{label} {fl}")
            else:
                _ = boxes[hashmap].pop(i)
                boxes[hashmap].insert(i, f"{label} {fl}")
        if f == "-":
            try:
                i = [i for i, x in enumerate(boxes[hashmap]) if x.split()[0] == label][0]
            except IndexError:
                pass
            else:
                _ = boxes[hashmap].pop(i)
    return boxes


def sum_focal_power_of_a_box(box: List[str], box_number: int) -> int:
    """
    Calculate the focal power of a box

    (box_number + 1) * (index in list + 1) * focal length
    :param box:  list of lenses in the current box
    :param box_number: number of the current box
    :return: power of the box
    """
    return sum([(i + 1) * int(x.split()[1]) * (box_number + 1) for i, x in enumerate(box)])


def get_total_focusing_power(operations: List[str]) -> int:
    """
    Organise the lens and find the total power of the system

    :param operations: list of operations to carry out
    :return: the total power of the lens after being organised
    """
    boxes = organise_lenses(operations)
    return sum([sum_focal_power_of_a_box(box, n) for n, box in boxes.items()])


def solve(data: List[str], part: str = "a") -> int:
    """
    Solve the problem for day 1
    :param data: input data
    :param part: which part of the problem to solve - 'a' or 'b'
    :return: solution
    """
    if part == "a":
        return sum([get_hash(i) for i in data[0].split(",")])
    else:
        return get_total_focusing_power(data[0].split(","))
