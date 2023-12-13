import functools
from collections import Counter
from typing import List

CARDS = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
RANK_TYPES = {
    "five of kind": 6,
    "four of kind": 5,
    "full house": 4,
    "three of kind": 3,
    "two pairs": 2,
    "one pair": 1,
    "high card": 0,
}


def get_rank_type(hand: str) -> str:
    """
    Get the rank type of the hand
    :param hand: the input hand of cards
    :return: the rank type name
    """
    counts = Counter(hand)
    max_n = max(counts.values())
    if max_n == 5:
        return "five of kind"
    if max_n == 4:
        return "four of kind"
    if max_n == 3 and 2 in counts.values():
        return "full house"
    if max_n == 3:
        return "three of kind"
    if list(counts.values()).count(2) == 2:
        return "two pairs"
    if max_n == 2:
        return "one pair"
    return "high card"


def compare_hands_of_same_type(hand1: str, hand2: str) -> int:
    """
    If two hands have the same rank type - they can be split by comparing high cards from start of the hand

    This function is used as a custom sorting function with sorted()
    :param hand1: first hand to compare
    :param hand2: second hand to compare
    :return: 1 if hand1 > hand2 else -1
    """
    for c1, c2 in zip(list(hand1), list(hand2)):
        if CARDS.index(c1) < CARDS.index(c2):
            return -1
        if CARDS.index(c2) < CARDS.index(c1):
            return 1
    raise ValueError("Cannot distinguish two hands!")


def rank_hands(hands: List[str]) -> List[str]:
    """
    Given a list of hands, rank them so that the best hand is first
    :param hands: the list of hands
    :return: a ranked list of hands
    """
    hand_types = [get_rank_type(h) for h in hands]
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
                sorted_tied_hands = sorted(tied_hands, key=functools.cmp_to_key(compare_hands_of_same_type))
                final_ranking.extend(sorted_tied_hands)
    return final_ranking


def calculate_hand_winnings(data: List[str]) -> int:
    """
    Determine the total winnings of the hand which is (N - rank) * bid where N is number of hands and rank is the index
    after sorting with best hand first

    :param data: input list of hands and bids
    :return: total winnings
    """
    hands_dict = {h.split(" ")[0]: int(h.split(" ")[1]) for h in data}
    ranked_hands = rank_hands(list(hands_dict.keys()))
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
        return 1
