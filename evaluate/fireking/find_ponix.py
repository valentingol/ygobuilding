"""When Ponix in hand."""

from typing import List, Tuple


def case_ponix_hand(
    res: List[str],
    hand: List[dict],
    hand_names: List[str],
    deck: List[dict],
) -> Tuple[List[str], List[dict], List[str], List[dict]]:
    """Case Ponix in hand."""
    if (
        sum(["fireking" in card["specs"] for card in hand if card["kind"] == "monster"])
        >= 2
    ):
        res.append("good engine")
    else:
        fire_monsters = [
            card
            for card in hand
            if card["kind"] == "monster" and card["attribute"] == "fire"
        ]
        if len(fire_monsters) >= 2:  # Ponix + another fire monster
            # Remove the other fire card
            ind = hand_names.index(fire_monsters[0]["name"])
            hand.pop(ind)
            hand_names.pop(ind)
            res.append("good engine")
        elif "nadir_servant" in hand_names and "maximus" not in hand_names:
            res.append("good engine")
        else:
            res.append("middle engine")
    return res, hand, hand_names, deck


def case_one_for_one_hand(
    res: List[str],
    hand: List[dict],
    hand_names: List[str],
    deck: List[dict],
) -> Tuple[List[str], List[dict], List[str], List[dict]]:
    """Case One for One in hand."""
    monsters = [card for card in hand if card["kind"] == "monster"]
    if len(monsters) == 0:
        # Cannot use One for One
        return res, hand, hand_names, deck
    handtraps = [
        card
        for card in hand
        if card["kind"] == "monster" and "handtrap" in card["specs"]
    ]
    firekings = [
        card
        for card in hand
        if card["kind"] == "monster" and "fireking" in card["specs"]
    ]
    others = [
        card
        for card in hand
        if card["kind"] == "monster"
        and "fireking" not in card["specs"]
        and "handtrap" not in card["specs"]
    ]
    if len(others) >= 1:
        ind = hand_names.index(others[0]["name"])
        hand.pop(ind)
        hand_names.pop(ind)
    elif len(firekings) >= 2 or (len(firekings) == 1 and len(handtraps) < 2):
        # Use One for One on fireking
        ind = hand_names.index(firekings[0]["name"])
        hand.pop(ind)
        hand_names.pop(ind)
    elif len(handtraps) >= 1:
        ind = hand_names.index(handtraps[0]["name"])
        hand.pop(ind)
        hand_names.pop(ind)
    else:
        # Cannot use One for One
        return res, hand, hand_names, deck
    # Add Ponix (in field but we consider it in hand to simplify)
    deck_names = [card["name"] for card in deck]
    hand.append(deck.pop(deck_names.index("ponix")))
    hand_names.append("ponix")
    return res, hand, hand_names, deck


def case_oss_hand(
    res: List[str],
    hand: List[dict],
    hand_names: List[str],
    deck: List[dict],
) -> Tuple[List[str], List[dict], List[str], List[dict]]:
    """Case Original Sinful Spoil in hand."""
    spells = [card for card in hand if card["kind"] == "spell"]
    n_continuous = len([card for card in spells if card["type"] == "continuous"])
    n_field = len([card for card in spells if card["type"] == "field"])
    if n_continuous == 0 and n_field == 0:
        # Require a summonable monster to use OSS
        handtraps = [
            card
            for card in hand
            if card["kind"] == "monster"
            and card["level"] <= 4
            and "handtrap" in card["specs"]
        ]
        firekings = [
            card
            for card in hand
            if card["kind"] == "monster"
            and card["level"] <= 4
            and "fireking" in card["specs"]
        ]
        others = [
            card
            for card in hand
            if card["kind"] == "monster"
            and card["level"] <= 4
            and "fireking" not in card["specs"]
            and "handtrap" not in card["specs"]
        ]
        if len(others) >= 1:
            # Use OSS on other monster
            ind = hand_names.index(others[0]["name"])
            hand.pop(ind)
            hand_names.pop(ind)
        if len(firekings) >= 2 or (len(firekings) == 1 and len(handtraps) < 2):
            # Use OSS on fireking
            ind = hand_names.index(firekings[0]["name"])
            hand.pop(ind)
            hand_names.pop(ind)
        elif len(handtraps) >= 1:
            # Use OSS on handtrap
            ind = hand_names.index(handtraps[0]["name"])
            hand.pop(ind)
            hand_names.pop(ind)
        else:
            # Cannot use OSS
            return res, hand, hand_names, deck
    deck_names = [card["name"] for card in deck]
    hand.append(deck.pop(deck_names.index("ponix")))
    hand_names.append("ponix")
    return res, hand, hand_names, deck


def case_nadir_hand(
    res: List[str],
    hand: List[dict],
    hand_names: List[str],
    deck: List[dict],
) -> Tuple[List[str], List[dict], List[str], List[dict]]:
    """Case Nadir Servant in hand."""
    if "maximus" in hand_names:
        # Cannot use Nadir Servant
        return res, hand, hand_names, deck
    # Use Nadir Servant to get Ponix
    deck_names = [card["name"] for card in deck]
    hand.append(deck.pop(deck_names.index("ponix")))
    hand_names.append("ponix")
    # Draw with Garura
    hand.append(deck[0])
    hand_names.append(deck[0]["name"])
    deck = deck[1:]
    res.append("good engine")
    return res, hand, hand_names, deck


def case_no_ponix_hand(
    res: List[str],
    hand: List[dict],
    hand_names: List[str],
    deck: List[dict],
) -> Tuple[List[str], List[dict], List[str], List[dict]]:
    """Case no Ponix in hand."""
    fire_monster = [
        card
        for card in hand
        if card["kind"] == "monster" and card["attribute"] == "fire"
    ]
    if (
        "fk_island" in hand_names
        or "fk_sanctuary" in hand_names
        and len(fire_monster) >= 2
    ):
        if "garunix" in hand_names:
            res.append("good engine")
        else:
            res.append("middle engine")
    if "kirin" in hand_names and "garunix" in hand_names and len(fire_monster) >= 3:
        res.append("middle engine")
    return res, hand, hand_names, deck
