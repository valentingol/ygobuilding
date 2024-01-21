"""Main entry point for the fireking evaluation."""
from typing import List

from evaluate.fireking.find_ponix import (
    case_nadir_hand,
    case_no_ponix_hand,
    case_one_for_one_hand,
    case_oss_hand,
    case_ponix_hand,
)

ORDER = [
    "bad engine",
    "middle engine",
    "good engine",
    "1 handtrap",
    "2+ handtraps",
    "dodge droll",
]


def score_hand(hand: List[dict], deck: List[dict]) -> List[str]:
    """Score a hand from fireking deck."""
    res = []
    hand_names = [card["name"] for card in hand]
    # Dodge Droll ?
    if (
        ("fk_island" in hand_names or "fk_sanctuary" in hand_names)
        and sum(["fireking" in card["specs"] for card in hand]) >= 2
    ) or ("called_by" in hand_names or "triple_tactics" in hand_names):
        res.append("dodge droll")

    # Use Tenki if possible
    if "tenki" in hand_names:
        deck_names = [card["name"] for card in deck]
        arvata = deck.pop(deck_names.index("arvata"))
        hand.append(arvata)
        hand_names.append("arvata")

    # Get Ponix with one for one or original sinful spoil
    if "ponix" not in hand_names:
        if "one_for_one" in hand_names:
            res, hand, hand_names, deck = case_one_for_one_hand(
                res, hand, hand_names, deck
            )
        elif "original_sinful_spoil" in hand_names:
            res, hand, hand_names, deck = case_oss_hand(res, hand, hand_names, deck)

    # Use Ponix NS before using Nadir Servant if possible
    if "ponix" in hand_names:
        res, hand, hand_names, deck = case_ponix_hand(res, hand, hand_names, deck)
    elif "nadir_servant" in hand_names:
        res, hand, hand_names, deck = case_nadir_hand(res, hand, hand_names, deck)
    else:
        # No Ponix
        res, hand, hand_names, deck = case_no_ponix_hand(res, hand, hand_names, deck)

    # Handtraps ?
    n_handtraps = sum(["handtrap" in card["specs"] for card in hand])
    if n_handtraps == 1:
        res.append("1 handtrap")
    elif n_handtraps >= 2:
        res.append("2+ handtraps")

    # Good engine ?
    if "good engine" not in res and "middle engine" not in res:
        res.append("bad engine")
    return res
