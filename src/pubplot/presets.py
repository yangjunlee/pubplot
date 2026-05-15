"""Scientific-plot presets built on top of pubplot's core styling helpers."""

from __future__ import annotations

from collections.abc import Sequence

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.colorbar import Colorbar

from .style import polish_axes, style_legend


def style_dos_plot(
    ax: Axes,
    *,
    energy_axis: str = "x",
    fermi_level: float = 0.0,
    xlabel: str | None = r"$E - E_F$ (eV)",
    ylabel: str | None = "DOS (states/eV)",
    show_fermi_level: bool = True,
    legend: bool = True,
) -> Axes:
    """Style a density-of-states or projected-DOS plot."""
    polish_axes(ax, xlabel=xlabel, ylabel=ylabel, grid=False)

    if show_fermi_level:
        if energy_axis == "x":
            ax.axvline(fermi_level, color="0.15", linewidth=1.1, linestyle="--", zorder=0)
        elif energy_axis == "y":
            ax.axhline(fermi_level, color="0.15", linewidth=1.1, linestyle="--", zorder=0)
        else:
            raise ValueError("energy_axis must be 'x' or 'y'.")

    if legend:
        style_legend(ax)
    return ax


def style_band_structure(
    ax: Axes,
    *,
    kpoints: Sequence[float] | None = None,
    labels: Sequence[str] | None = None,
    fermi_level: float = 0.0,
    ylabel: str = r"$E - E_F$ (eV)",
    show_fermi_level: bool = True,
) -> Axes:
    """Style an electronic band-structure axis."""
    polish_axes(ax, ylabel=ylabel, grid=False)

    if kpoints is not None:
        for xpos in kpoints:
            ax.axvline(xpos, color="0.75", linewidth=0.8, zorder=0)
        if labels is not None:
            if len(kpoints) != len(labels):
                raise ValueError("kpoints and labels must have the same length.")
            ax.set_xticks(list(kpoints), list(labels))

    if show_fermi_level:
        ax.axhline(fermi_level, color="0.15", linewidth=1.1, linestyle="--", zorder=0)

    return ax


def style_convergence_plot(
    ax: Axes,
    *,
    xlabel: str = "Iteration",
    ylabel: str = "Residual",
    tolerance: float | None = None,
    log_y: bool = True,
    legend: bool = True,
) -> Axes:
    """Style an iterative convergence or parameter-convergence plot."""
    polish_axes(ax, xlabel=xlabel, ylabel=ylabel, grid=True)
    if log_y:
        ax.set_yscale("log")
    if tolerance is not None:
        ax.axhline(tolerance, color="0.2", linewidth=1.2, linestyle=":", label="tolerance")
    if legend:
        style_legend(ax)
    return ax


def style_heatmap(
    ax: Axes,
    *,
    cbar: Colorbar | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    cbar_label: str | None = None,
    title: str | None = None,
) -> Axes:
    """Style a heatmap axis and optional colorbar."""
    polish_axes(ax, xlabel=xlabel, ylabel=ylabel, title=title, minor_ticks=False)
    if cbar is not None:
        if cbar_label is not None:
            cbar.set_label(cbar_label)
        cbar.ax.tick_params(which="major", direction="in", length=4.5, width=1.0)
    return ax


def demo_pdos(ax: Axes | None = None) -> Axes:
    """Create a small synthetic PDOS-like demo for documentation and smoke tests."""
    import numpy as np

    if ax is None:
        _, ax = plt.subplots()

    energy = np.linspace(-6.0, 4.0, 600)
    mn_d = 1.6 * np.exp(-0.5 * ((energy + 1.2) / 0.55) ** 2)
    se_p = 1.0 * np.exp(-0.5 * ((energy + 2.4) / 0.80) ** 2)
    hybrid = 0.45 * np.exp(-0.5 * ((energy - 0.5) / 0.45) ** 2)

    ax.plot(energy, mn_d, label="Mn $d$")
    ax.plot(energy, se_p, label="Se $p$")
    ax.plot(energy, hybrid, label="hybridized")
    style_dos_plot(ax)
    return ax
