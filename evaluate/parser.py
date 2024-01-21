# Copyright (c) 2024 Valentin Goldite. All Rights Reserved.
"""Parser for command line arguments."""
import argparse
from typing import Tuple


def parse_args() -> Tuple[str, int, str]:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n", "--number", help="Number of hands to evaluate", default=100_000, type=int
    )
    parser.add_argument(
        "--name", help="Deck name (same as evaluate/ sub-folder names)", type=str
    )
    parser.add_argument(
        "--configs", help="Configurations file", type=str, required=True
    )
    args = parser.parse_args()
    return args.name, args.number, args.configs
