# Copyright (c) 2024 Valentin Goldite. All Rights Reserved.
"""Main entry point for hand evaluation."""
import os
import random
from datetime import datetime

from evaluate.decks import get_decks
from evaluate.parser import parse_args
from evaluate.plot import plot_save_results


def main() -> None:
    """Draw multiple hands, evaluate them and return the results."""
    deck_name, num_runs, configs_path = parse_args()
    # Get order and score_hand function
    score_hand = __import__(
        f"evaluate.{deck_name}.score", fromlist=["score_hand"]
    ).score_hand
    order = __import__(f"evaluate.{deck_name}.score", fromlist=["ORDER"]).ORDER

    decks, cfg_names = get_decks(base_deck=deck_name, configs_path=configs_path)
    all_results = []
    for i, cfg_name in enumerate(cfg_names):
        print(f"{cfg_name}:")
        original_deck = decks[i]
        results = {label: 0.0 for label in order}
        for seed in range(num_runs):
            # Shuffle the deck and draw a hand.
            deck = random.Random(seed).sample(original_deck, len(original_deck))
            hand, deck = deck[:5], deck[5:]
            label_list = score_hand(hand, deck)
            for label in label_list:
                results[label] += 1.0 / num_runs
        all_results.append(results)
        for label, result in results.items():
            print(f" - {label} hands: {result * 100:.1f}%")
        print()

    # Plot and save results
    now = datetime.now()
    date_string = now.strftime("%d_%m_%Y_%H:%M:%S")
    plot_save_results(
        results=all_results,
        labels=order,
        cfg_names=cfg_names,
        deck_name=deck_name,
        date_string=date_string,
    )
    # Save configs in results folder
    os.makedirs(f"results/{deck_name}/configs", exist_ok=True)
    os.system(f"cp {configs_path} results/{deck_name}/configs/{date_string}.txt")


if __name__ == "__main__":
    main()
