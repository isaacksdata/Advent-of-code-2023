from typing import List


def get_winning_numbers(card: str) -> List[int]:
    """
    Extract the winning numbers from the card
    :param card: input card data
    :return: list of winning numbers
    """
    winning_numbers = card.split(" | ")[0].split(": ")[1].split()
    return list(map(int, winning_numbers))


def get_trial_numbers(card: str) -> List[int]:
    """
    Extract the trial numbers from the card
    :param card: input card data
    :return: list of trial numbers
    """
    trial_numbers = card.split(" | ")[1].split()
    return list(map(int, trial_numbers))


def get_matches(winning_numbers: List[int], trial_numbers: List[int]) -> int:
    """
    Count the overlap between the winning numbers and trial numbers
    :param winning_numbers: list of numbers
    :param trial_numbers: list of numbers
    :return: length of intersection
    """
    return len([x for x in trial_numbers if x in winning_numbers])


def score_cards(data: List[str]) -> int:
    """
    Calculate the score of each card and sum

    1 point for first match and double the score for each subsequent match
    :param data: input data
    :return: total score
    """
    total = 0
    for card in data:
        n = get_matches(get_winning_numbers(card), get_trial_numbers(card))
        if n > 0:
            score = 2 ** (n - 1)
            total += score
    return total


def solve(data: List[str], part: str = "a") -> int:
    """
    Solve the problem for day 1
    :param data: input data
    :param part: which part of the problem to solve - 'a' or 'b'
    :return: solution
    """
    if part == "a":
        return score_cards(data)
    else:
        return 1
