from typing import Dict
from typing import List


def create_map(data: List[str]) -> Dict[str, Dict[str, str]]:
    """
    Create a map from the input data

    Each primary key is a node and each node has a L and R node
    Example:
    ["AAA = (BBB, BBB)",
    "BBB = (AAA, ZZZ)",
    "ZZZ = (ZZZ, ZZZ)"]

            =

    {
        "AAA": {"L":"BBB", "R": "BBB"},
        "BBB": {"L":"AAA", "R": "ZZZ"},
        "ZZZ": {"L":"ZZZ", "R": "ZZZ"}
    }
    :param data: the input data
    :return: mapping dict
    """
    d = {}
    for node in data[2:]:
        n = node.split(" = ")[0]
        l = node.split(" = ")[1].split(", ")[0][1:]
        r = node.split(" = ")[1].split(", ")[1][:-1]
        d[n] = dict(L=l, R=r)
    return d


def get_moves(data: List[str]) -> List[str]:
    """
    Extract moves from the input data - first element
    :param data: input data
    :return: list of moves to follow
    """
    return list(data[0])


def traverse_map(mapping: Dict[str, Dict[str, str]], moves: List[str]) -> int:
    """
    Traverse the map by iterating over the moves and following the nodes through the mapping dict
    :param mapping: mapping dict from create_map()
    :param moves: moves from get_moves()
    :return: the number of moves taken to get from start_node to end_node
    """
    iterations = 0  # Initialize the iteration counter
    start_node = "AAA"
    end_node = "ZZZ"
    node = start_node
    while True:
        move = moves[iterations % len(moves)]
        node = mapping[node][move]
        # print(f"Moved to {node}")
        # Increment the iteration counter
        iterations += 1

        # You can add a condition to break the loop when needed
        # For example, break the loop after a certain number of iterations
        if node == end_node:
            break
    return iterations


def solve(data: List[str], part: str = "a") -> int:
    """
    Solve the problem for day 1
    :param data: input data
    :param part: which part of the problem to solve - 'a' or 'b'
    :return: solution
    """
    if part == "a":
        return traverse_map(mapping=create_map(data), moves=get_moves(data))
    else:
        return 1
