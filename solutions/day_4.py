from functools import cache
from typing import List
from typing import Tuple

import tqdm


def get_card_number(card: str) -> str:
    """
    Extract card number from the card string
    :param card: card string
    :return: the card number in form of "Card  x"
    """
    return card.split(": ")[0]


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


def get_card_id(card: str) -> int:
    """
    Get just the numeric card ID from the card string
    :param card: card string
    :return: card ID
    """
    card_id = get_card_number(card)
    return int(card_id.split("Card ")[1])


@cache
def analyse_card(card: str, original_cards: Tuple[str]) -> int:
    """
    Recursive function for getting total cards per original starter card

    This funtion uses the cache dictionary to store the results of each card so each card only has to be
    analysed once
    :param card: card string
    :param original_cards: the original cards list
    :return: total number of cards received due to input card
    """
    total = 0
    current_idx = get_card_id(card)
    n = get_matches(get_winning_numbers(card), get_trial_numbers(card))
    total += n
    if n > 0:
        new_cards = [
            c for c in original_cards if any([get_card_id(c) == i for i in range(current_idx + 1, current_idx + 1 + n)])
        ]
        for new_card in new_cards:
            total += analyse_card(new_card, original_cards)
    return total


def count_cards(data: List[str]) -> int:
    """
    Count the total number of cards received
    :param data: input starter cards
    :return: total number of cards
    """
    original_cards = tuple(data.copy())
    totals = []
    for card in tqdm.tqdm(data):
        card_total = analyse_card(card, original_cards)
        totals.append(card_total)
    return sum(totals) + len(data)


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
        return count_cards(data)
