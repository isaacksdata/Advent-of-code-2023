from math import prod
from typing import Dict
from typing import List
from typing import Tuple

COLOURS = ["red", "green", "blue"]


def get_game_id(game: str) -> int:
    """
    Get the ID for a specific game.

    E.g. "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
    ID = 1
    :param game: the game string
    :return: ID of the game as int
    """
    return int(game.split(":")[0].split()[1])


def split_turns(game: str) -> List[str]:
    """
    Split the game into turns
    :param game: the game string
    :return: the list of turns
    """
    return game.split(":")[1].split(";")


def count_colours(turn: str) -> Dict[str, int]:
    """
    For a given turn of a game, extract the colour counts
    :param turn: the input turn string
    :return: a dictionary of colour name to counts
    """
    values = turn.split(",")
    counts = {}
    for v in values:
        v = v.strip()
        for c in COLOURS:
            if c in v:
                counts[c] = int(v.split(" ")[0])
    return counts


def solve_game(game: str, colour_limits: Dict[str, int]) -> Tuple[int, bool]:
    """
    Solve for a particular input game string and determine if the game is possible based on imposed limits
    on number of balls of each colour
    :param game: input game string
    :param colour_limits: limits on how many balls of each colour are present
    :return: the game ID and whether the game is possible
    """
    game_id = get_game_id(game)
    turns = split_turns(game)
    for turn in turns:
        counts = count_colours(turn)
        for c in counts:
            if counts[c] > colour_limits[c]:
                return game_id, False
    return game_id, True


def calculate_game_power(game: str) -> int:
    """
    The power of the game is the product of the minimum number of balls of each colour required to make the game
    possible
    :param game: game string
    :return: power of the game
    """
    turns = split_turns(game)
    maxes = {c: 0 for c in COLOURS}
    for turn in turns:
        counts = count_colours(turn)
        for c, v in counts.items():
            if v > maxes[c]:
                maxes[c] = v
    return prod(maxes.values())


def solve(data: List[str], colour_limits: Dict[str, int], part: str = "a") -> int:
    """
    Entrypoint for solving day 2
    :param data: input data
    :param colour_limits: limits of number of balls for each colour
    :param part: which part of the puzzle
    :return: the solution
    """
    if part == "a":
        possible_game_ids = []
        for game in data:
            i, possible = solve_game(game, colour_limits)
            if possible:
                possible_game_ids.append(i)
        return sum(possible_game_ids)
    elif part == "b":
        powers = [calculate_game_power(game) for game in data]
        return sum(powers)
    else:
        raise ValueError("Unexpected part!")
