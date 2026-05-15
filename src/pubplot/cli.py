"""Command-line entry points for pubplot examples."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from . import emphasize_zero_axes, polish_axes, publication_style, save_publication_figure, style_legend


def build_demo(output: Path) -> list[Path]:
    """Build a synthetic multi-curve figure and save it."""
    x = np.linspace(0.0, 8.0, 500)

    with publication_style(font_scale=1.05, column="double", aspect="wide", palette="colorblind"):
        fig, ax = plt.subplots()
        ax.plot(x, np.exp(-x / 4.0) * np.sin(2.5 * x), label=r"$A e^{-x/\tau}\sin(\omega x)$")
        ax.plot(x, 0.65 * np.exp(-x / 5.0) * np.cos(2.5 * x), label=r"$B e^{-x/\tau}\cos(\omega x)$")
        ax.plot(x, 0.20 * np.sin(6.0 * x), label="weak oscillation")

        polish_axes(
            ax,
            xlabel="Time (ps)",
            ylabel="Normalized signal",
            grid=False,
        )
        emphasize_zero_axes(ax, y=True)
        style_legend(ax, outside="top", ncol=3, frameon=False)
        fig.tight_layout(rect=(0.0, 0.0, 1.0, 0.90))
        return save_publication_figure(fig, output)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create a pubplot demonstration figure.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("figures/pubplot_demo"),
        help="Output path without extension.",
    )
    args = parser.parse_args(argv)

    written = build_demo(args.output)
    for path in written:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
