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

        iterations += 1

        if node == end_node:
            break
    return iterations


def gcd(x: int, y: int) -> int:
    """
    Calculate the Greatest Common Divisor (GCD) between two numbers following Euclids algorithm

    The algorithm is based on the observation that if a>b, then the common divisors of b are the same as the
    common divisors of b and a mod b. In other words:
    gcd(a,b)=gcd(b,amodb)

    Initialization:
    Start with two positive integers a and b where a>b.
    If b is zero, then the GCD is a

    Iteration:
    Calculate the remainder of a divided by b: r=a mod b.
    Set a to b and b to r
    Repeat until b becomes zero

    Termination:
    When b becomes zero, the current value of a is the GCD

    :param x: first number
    :param y: second number
    :return: gcd
    """
    while y:
        x, y = y, x % y
    return x


def lcm(x: int, y: int) -> int:
    """
    Find the lowest common multiple of two numbers

    Uses Bézout's Identity formula which states that prod(GCD(x, y), LCM(x, y)) == prod(x, y)
    :param x:
    :param y:
    :return:
    """
    return (x * y) // gcd(x, y)


def lcm_of_list(numbers: List[int]) -> int:
    """
    Calculate the Lowest common multiple of a list of numbers
    :param numbers: input numbers
    :return: LCM
    """
    if len(numbers) == 0:
        raise ValueError("The list is empty. Please provide a non-empty list of numbers.")

    result = numbers[0]

    for num in numbers[1:]:
        result = lcm(result, num)

    return result


def traverse_multi_map(mapping: Dict[str, Dict[str, str]], moves: List[str]) -> int:
    """
    Traverse the map by iterating over the moves and following the nodes through the mapping dict

    Once each node reaches a node ending in end_pat, the iteration is logged and the node is removed from the list
    This logic works on the assumption that once a path hits the end node it then behaves as an oscillator and reaches
    the same end node again in N steps. So if you find time to hit end node for each start node then the LCM is the
    number of steps till all nodes simultaneously reach the end node

    :param mapping: mapping dict from create_map()
    :param moves: moves from get_moves()
    :return: the number of moves taken to get from start_node to end_node
    """
    iterations = 0  # Initialize the iteration counter
    start_pat = "A"
    end_pat = "Z"
    end_steps = []
    nodes = [node for node in mapping.keys() if node.endswith(start_pat)]
    while True:
        move = moves[iterations % len(moves)]
        nodes = [mapping[node][move] for node in nodes]
        iterations += 1
        reached_end = [node.endswith(end_pat) for node in nodes]
        if any(reached_end):
            end_steps.append(iterations)
            nodes = [n for i, n in zip(reached_end, nodes) if not i]
            if len(nodes) == 0:
                break
    return lcm_of_list(end_steps)


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
        return traverse_multi_map(mapping=create_map(data), moves=get_moves(data))
