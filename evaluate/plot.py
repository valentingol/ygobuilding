# Copyright (c) 2024 Valentin Goldite. All Rights Reserved.
"""Matplotlib functions for plotting results."""
import os
from typing import Dict, List

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure


def plot_save_results(
    results: List[Dict[int, float]],
    labels: List[str],
    cfg_names: List[str],
    deck_name: str,
    date_string: str,
) -> None:
    """Plot and save the results of the evaluation."""
    fig = plot_results(results=results, labels=labels, cfg_names=cfg_names)
    save_plot(fig=fig, deck_name=deck_name, date_string=date_string)
    plt.show()


def save_plot(fig: Figure, deck_name: str, date_string: str) -> None:
    """Save a matplotlib figure."""
    os.makedirs(f"results/{deck_name}/plots", exist_ok=True)
    fig.savefig(f"results/{deck_name}/plots/{date_string}.png")


def plot_results(
    results: List[Dict[int, float]],
    labels: List[str],
    cfg_names: List[str],
) -> Figure:
    """Plot the results of the evaluation."""
    # Empirically determined width for any number of configs.
    width = min(0.9, 0.4 + len(results) / 20)

    fig, ax = plt.subplots(figsize=(16, 8))
    ind = np.arange(len(results[0]))
    for i, (result, cfg_name) in enumerate(zip(results, cfg_names)):
        ax.bar(
            ind + (width * i) / (len(results) - 1) - width / 2,
            result.values(),
            width / (len(results) - 1),
            label=cfg_name,
        )
    ax.set_title("Scores of hands")
    ax.set_ylabel("Probability")
    ax.set_xticks(ind)
    ax.set_xticklabels([lab.capitalize() for lab in labels])
    ax.legend()
    fig.tight_layout()
    return fig
