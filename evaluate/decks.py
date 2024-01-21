# Copyright (c) 2024 Valentin Goldite. All Rights Reserved.
"""Functions for getting decks from a base deck and configs."""
from typing import List, Tuple

import yaml


def flatten_deck(deck: List[str]) -> List[str]:
    """Return a flattened deck."""
    flat_deck = []
    for card in deck:
        if card.startswith("1"):
            flat_deck.append(card[1:].strip())
        elif card.startswith("2"):
            flat_deck.extend([card[1:].strip()] * 2)
        elif card.startswith("3"):
            flat_deck.extend([card[2:].strip()] * 3)
        else:
            flat_deck.append(card.strip())
    return flat_deck


def name_to_cards(cards: dict, base_deck: str, deck_str: List[str]) -> List[List]:
    """Return a deck with cards instead of names."""
    for card_name in deck_str:
        if card_name not in cards:
            raise ValueError(
                f"Card name '{card_name}' not found in cards/{base_deck} "
                "or cards/generics."
            )
    return [cards[card_name] for card_name in deck_str]


def add_card(
    current_deck_str: List[str],
    card_name: str,
) -> None:
    """Add a card to a deck."""
    if card_name[0] in ("1", "2", "3"):
        number, card_name = int(card_name[0]), card_name[1:].strip()
    else:
        number = 1
    for _ in range(number):
        current_deck_str.append(card_name)


def remove_card(
    current_deck_str: List[str],
    card_name: str,
    config_names: List[str],
) -> None:
    """Remove a card from a deck."""
    if card_name[0] in ("1", "2", "3"):
        number, card_name = int(card_name[0]), card_name[1:].strip()
    else:
        number = 1
    try:
        for _ in range(number):
            # Remove one card
            current_deck_str.remove(card_name)
    except ValueError as err:
        raise ValueError(
            f"Card {card_name} not found in base deck (error in config "
            f"'{config_names[-1]}', requires {number} card(s) with this name)."
        ) from err


def get_decks(base_deck: str, configs_path: str) -> Tuple[List[List], List[str]]:
    """Return all decks and their names."""
    # Get cards
    with open("cards/generics.yaml", encoding="utf-8") as file:
        cards = yaml.safe_load(file)
    with open(f"cards/{base_deck}.yaml", encoding="utf-8") as file:
        other_cards = yaml.safe_load(file)
    cards.update(other_cards)
    # Get str deck
    with open("configs/base.yaml", encoding="utf-8") as file:
        deck_str = yaml.safe_load(file)[base_deck]
    flat_deck_str = flatten_deck(deck_str)
    for card_name in flat_deck_str:
        if card_name not in cards:
            raise ValueError(
                f"Card name '{card_name}' in configs/base.yaml [{base_deck}] not "
                f"found in cards/{base_deck} or cards/generics."
            )
    # Parse configs and build decks
    with open(configs_path, encoding="utf-8") as file:
        lines = file.readlines()
    assert lines[0].startswith(
        "##"
    ), "First line of configs file must be '## <cfg_name>'."
    decks, config_names = [], []
    current_deck_str = flat_deck_str.copy()
    for line in lines:
        if line.startswith("##"):
            config_names.append(line[2:].strip())
            if len(config_names) > 1:
                decks.append(name_to_cards(cards, base_deck, current_deck_str.copy()))
                current_deck_str = flat_deck_str.copy()
        elif line.startswith("#") or line.strip() in ("", "\n"):
            continue
        elif line.startswith("-"):
            card_name = line[1:].strip()
            remove_card(
                current_deck_str=current_deck_str,
                card_name=card_name,
                config_names=config_names,
            )
        elif line.startswith("+"):
            card_name = line[1:].strip()
            add_card(current_deck_str=current_deck_str, card_name=card_name)
        else:
            raise ValueError(f"Invalid line in config '{config_names[-1]}': {line}")
    decks.append(name_to_cards(cards, base_deck, current_deck_str.copy()))

    return decks, config_names
