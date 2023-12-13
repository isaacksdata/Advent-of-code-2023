import functools
from collections import Counter
from typing import List

CARDS = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
CARDS_JOKER = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]
RANK_TYPES = {
    "five of kind": 6,
    "four of kind": 5,
    "full house": 4,
    "three of kind": 3,
    "two pairs": 2,
    "one pair": 1,
    "high card": 0,
}


def get_rank_type(hand: str, jokers: bool = False) -> str:
    """
    Get the rank type of the hand
    :param hand: the input hand of cards
    :param jokers: whether jokers are in the deck
    :return: the rank type name
    """
    counts = Counter(hand)
    n_jokers = counts.get("J", 0) if jokers else 0
    if n_jokers == 5:
        return "five of kind"
    if n_jokers > 0:
        _ = counts.pop("J")
    max_n = max(counts.values())
    if max_n == 5:
        return "five of kind"
    if max_n == 4:
        if n_jokers > 0:
            return "five of kind"
        return "four of kind"
    if max_n == 3 and 2 in counts.values():
        if n_jokers == 1:
            return "four of kind"
        if n_jokers > 1:
            return "five of kind"
        return "full house"
    if max_n == 3:
        if n_jokers == 1:
            return "four of kind"
        if n_jokers > 1:
            return "five of kind"
        return "three of kind"
    if list(counts.values()).count(2) == 2:
        if n_jokers == 1:
            return "full house"
        if n_jokers == 2:
            return "four of kind"
        if n_jokers > 2:
            return "five of kind"
        return "two pairs"
    if max_n == 2:
        if n_jokers == 1:
            return "three of kind"
        if n_jokers == 2:
            return "four of kind"
        if n_jokers > 2:
            return "five of kind"
        return "one pair"
    if n_jokers == 1:
        return "one pair"
    if n_jokers == 2:
        return "three of kind"
    if n_jokers == 3:
        return "four of kind"
    if n_jokers > 3:
        return "five of kind"
    return "high card"


def compare_hands_of_same_type(jokers: bool, hand1: str, hand2: str) -> int:
    """
    If two hands have the same rank type - they can be split by comparing high cards from start of the hand

    This function is used as a custom sorting function with sorted()
    :param jokers: whether jokers are in the deck
    :param hand1: first hand to compare
    :param hand2: second hand to compare
    :return: 1 if hand1 > hand2 else -1
    """
    card_ranks = CARDS_JOKER if jokers else CARDS
    for c1, c2 in zip(list(hand1), list(hand2)):
        if card_ranks.index(c1) < card_ranks.index(c2):
            return -1
        if card_ranks.index(c2) < card_ranks.index(c1):
            return 1
    raise ValueError("Cannot distinguish two hands!")


def rank_hands(hands: List[str], jokers: bool = False) -> List[str]:
    """
    Given a list of hands, rank them so that the best hand is first
    :param hands: the list of hands
    :param jokers: whether jokers are in the deck
    :return: a ranked list of hands
    """
    hand_types = [get_rank_type(h, jokers) for h in hands]
    hand_values = [RANK_TYPES[r] for r in hand_types]

    combined = list(zip(hands, hand_values))

    # Sort the combined list based on scores in descending order
    sorted_combined = sorted(combined, key=lambda x: x[1], reverse=True)

    # Separate the sorted pairs back into two lists
    sorted_hands, sorted_scores = zip(*sorted_combined)

    final_ranking = []
    for score in RANK_TYPES.values():
        if score in sorted_scores:
            idx = [i for i, s in enumerate(sorted_scores) if s == score]
            if len(idx) == 0:
                pass
            elif len(idx) == 1:
                final_ranking.append(sorted_hands[idx[0]])
            else:
                tied_hands = [h for i, h in enumerate(sorted_hands) if i in idx]
                sort_func = functools.partial(compare_hands_of_same_type, jokers)
                sorted_tied_hands = sorted(tied_hands, key=functools.cmp_to_key(sort_func))
                final_ranking.extend(sorted_tied_hands)
    return final_ranking


def calculate_hand_winnings(data: List[str], jokers: bool = False) -> int:
    """
    Determine the total winnings of the hand which is (N - rank) * bid where N is number of hands and rank is the index
    after sorting with best hand first

    :param data: input list of hands and bids
    :param jokers: whether jokers are in the deck
    :return: total winnings
    """
    hands_dict = {h.split(" ")[0]: int(h.split(" ")[1]) for h in data}
    ranked_hands = rank_hands(list(hands_dict.keys()), jokers)
    ms = len(ranked_hands)
    winnings = [(ms - i) * hands_dict[h] for i, h in enumerate(ranked_hands)]
    return sum(winnings)


def solve(data: List[str], part: str = "a") -> int:
    """
    Solve the problem for day 1
    :param data: input data
    :param part: which part of the problem to solve - 'a' or 'b'
    :return: solution
    """
    if part == "a":
        return calculate_hand_winnings(data)
    else:
        return calculate_hand_winnings(data, jokers=True)
