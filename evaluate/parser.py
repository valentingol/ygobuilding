# Copyright (c) 2024 Valentin Goldite. All Rights Reserved.
"""Parser for command line arguments."""
import argparse
from argparse import Namespace


def parse_args() -> Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n",
        "--num_runs",
        help="Number of hands to evaluate",
        default=100_000,
        type=int,
    )
    parser.add_argument(
        "-c",
        "--num_cards",
        help="Number of cards in hand",
        default=5,
        type=int,
    )
    parser.add_argument(
        "--name", help="Deck name (same as evaluate/ sub-folder names)", type=str
    )
    parser.add_argument(
        "--configs", help="Configurations file", type=str, required=True
    )
    args = parser.parse_args()
    return args
