"""Core Matplotlib styling helpers for publication-quality figures."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from contextlib import contextmanager
from cycler import cycler
from itertools import cycle, islice
from pathlib import Path
from typing import Literal

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.text import Text

ColumnSize = Literal["single", "double", "square", "wide"]
Aspect = Literal["golden", "square", "wide", "band"]
Palette = Literal["colorblind", "high_contrast", "grayscale", "journal"]

GOLDEN_RATIO = 0.61803398875

PAPER_WIDTHS_INCH = {
    "single": 3.45,
    "double": 7.10,
    "square": 3.45,
    "wide": 7.10,
}

PALETTES: dict[str, tuple[str, ...]] = {
    "colorblind": (
        "#0072B2",
        "#D55E00",
        "#009E73",
        "#CC79A7",
        "#E69F00",
        "#56B4E9",
        "#F0E442",
        "#000000",
    ),
    "high_contrast": (
        "#004488",
        "#BB5566",
        "#228833",
        "#AA3377",
        "#CCBB44",
        "#66CCEE",
        "#000000",
    ),
    "grayscale": (
        "#000000",
        "#444444",
        "#777777",
        "#AAAAAA",
        "#222222",
        "#666666",
    ),
    "journal": (
        "#1B1B1B",
        "#005AB5",
        "#DC3220",
        "#006400",
        "#7B3294",
        "#B8860B",
    ),
}

LINE_STYLES = ("-", "--", "-.", ":")
MARKERS = ("o", "s", "^", "D", "v", "P", "X", "*")

FIGURE_REVIEW_CHECKLIST = (
    "Can the main message be understood from the figure and caption alone?",
    "Are axis labels scientifically precise, with units where applicable?",
    "Are tick labels readable at the final manuscript size?",
    "Is one font family used consistently?",
    "Are panel labels consistent in style and position?",
    "Are matched axis scales used for comparable quantities?",
    "Are datasets distinguished by color plus marker or line style, not color alone?",
    "Does the legend avoid covering important data?",
    "Are annotations necessary, intuitive, and non-decorative?",
    "Are PDF/SVG vector outputs produced for manuscript use?",
)


def _repeat_to_length(values: Sequence[str], length: int) -> tuple[str, ...]:
    return tuple(islice(cycle(values), length))


def get_paper_size(
    column: ColumnSize = "single",
    aspect: Aspect | float = "golden",
    height: float | None = None,
) -> tuple[float, float]:
    """Return a figure size in inches for common paper layouts."""
    if column not in PAPER_WIDTHS_INCH:
        raise ValueError(f"Unknown column size {column!r}.")

    width = PAPER_WIDTHS_INCH[column]
    if height is not None:
        return width, float(height)

    if column == "square" or aspect == "square":
        ratio = 1.0
    elif aspect == "golden":
        ratio = GOLDEN_RATIO
    elif aspect == "wide":
        ratio = 0.50
    elif aspect == "band":
        ratio = 0.36
    elif isinstance(aspect, (int, float)):
        ratio = float(aspect)
    else:
        raise ValueError(f"Unknown aspect {aspect!r}.")

    return width, width * ratio


def _scaled_sizes(font_scale: float) -> dict[str, float]:
    base = 11.0 * font_scale
    return {
        "font.size": base,
        "axes.titlesize": 12.5 * font_scale,
        "axes.labelsize": 12.0 * font_scale,
        "xtick.labelsize": 10.5 * font_scale,
        "ytick.labelsize": 10.5 * font_scale,
        "legend.fontsize": 10.0 * font_scale,
        "legend.title_fontsize": 10.5 * font_scale,
        "figure.titlesize": 13.0 * font_scale,
    }


def rc_params(
    *,
    font_scale: float = 1.0,
    column: ColumnSize = "single",
    aspect: Aspect | float = "golden",
    palette: Palette = "colorblind",
    font_family: str | Sequence[str] = ("Arial", "Helvetica", "DejaVu Sans"),
    use_latex: bool = False,
) -> dict[str, object]:
    """Build publication-oriented Matplotlib rcParams."""
    width, height = get_paper_size(column=column, aspect=aspect)
    colors = PALETTES[palette]
    linestyles = _repeat_to_length(LINE_STYLES, len(colors))

    params: dict[str, object] = {
        "figure.figsize": (width, height),
        "figure.dpi": 120,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.03,
        "font.family": font_family,
        "mathtext.fontset": "dejavusans",
        "text.usetex": use_latex,
        "axes.linewidth": 1.2,
        "axes.edgecolor": "black",
        "axes.facecolor": "white",
        "axes.grid": False,
        "axes.prop_cycle": cycler(color=colors) + cycler(linestyle=linestyles),
        "lines.linewidth": 2.0,
        "lines.markersize": 6.0,
        "lines.markeredgewidth": 1.0,
        "patch.linewidth": 1.0,
        "xtick.direction": "in",
        "ytick.direction": "in",
        "xtick.major.size": 5.5,
        "ytick.major.size": 5.5,
        "xtick.minor.size": 3.0,
        "ytick.minor.size": 3.0,
        "xtick.major.width": 1.2,
        "ytick.major.width": 1.2,
        "xtick.minor.width": 1.0,
        "ytick.minor.width": 1.0,
        "xtick.top": True,
        "ytick.right": True,
        "legend.frameon": True,
        "legend.framealpha": 0.92,
        "legend.edgecolor": "0.3",
        "legend.fancybox": False,
        "legend.borderpad": 0.35,
        "legend.handlelength": 2.2,
        "legend.handletextpad": 0.55,
        "legend.labelspacing": 0.35,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
    }
    params.update(_scaled_sizes(font_scale))
    return params


@contextmanager
def publication_style(**kwargs: object):
    """Temporarily apply publication-oriented Matplotlib rcParams."""
    with mpl.rc_context(rc=rc_params(**kwargs)):
        yield


def _iter_axes(fig: Figure | None, axes: Axes | Iterable[Axes] | None) -> list[Axes]:
    if axes is None:
        return list(fig.axes) if fig is not None else []
    if isinstance(axes, Axes):
        return [axes]
    return list(axes)


def set_distinguishable_cycle(
    ax: Axes | None = None,
    *,
    palette: Palette = "colorblind",
    use_markers: bool = False,
    grayscale_safe: bool = False,
) -> None:
    """Set a color, line-style, and optional marker cycle."""
    colors = PALETTES["grayscale" if grayscale_safe else palette]
    style_cycle = cycler(color=colors) + cycler(linestyle=_repeat_to_length(LINE_STYLES, len(colors)))
    if use_markers:
        style_cycle = style_cycle + cycler(marker=_repeat_to_length(MARKERS, len(colors)))

    target = ax if ax is not None else plt.gca()
    target.set_prop_cycle(style_cycle)


def apply_marker_edges(
    ax: Axes,
    *,
    edgecolor: str = "0.15",
    linewidth: float = 0.8,
    apply_to_lines: bool = True,
    apply_to_collections: bool = True,
) -> Axes:
    """Add dark marker outlines for print and grayscale readability."""
    if apply_to_lines:
        for line in ax.lines:
            marker = line.get_marker()
            if marker not in (None, "", "None", "none", " "):
                line.set_markeredgecolor(edgecolor)
                line.set_markeredgewidth(linewidth)

    if apply_to_collections:
        for collection in ax.collections:
            if hasattr(collection, "set_edgecolor"):
                collection.set_edgecolor(edgecolor)
            if hasattr(collection, "set_linewidth"):
                collection.set_linewidth(linewidth)

    return ax


def emphasize_zero_axes(
    ax: Axes,
    *,
    x: bool = False,
    y: bool = True,
    color: str = "0.15",
    linewidth: float = 1.1,
    linestyle: str = "-",
    zorder: float = 0.5,
) -> Axes:
    """Draw clean reference lines at x=0 and/or y=0 without adding a full grid."""
    if x:
        ax.axvline(0.0, color=color, linewidth=linewidth, linestyle=linestyle, zorder=zorder)
    if y:
        ax.axhline(0.0, color=color, linewidth=linewidth, linestyle=linestyle, zorder=zorder)
    return ax


def match_axis_limits(
    axes: Iterable[Axes],
    *,
    axis: Literal["x", "y", "both"] = "both",
    margin_fraction: float = 0.0,
    symmetric: bool = False,
) -> None:
    """Match axis limits across panels that compare the same quantity."""
    axis_list = list(axes)
    if not axis_list:
        return

    def merged_limits(getter_name: str) -> tuple[float, float]:
        limits = [getattr(ax, getter_name)() for ax in axis_list]
        low = min(limit[0] for limit in limits)
        high = max(limit[1] for limit in limits)
        if symmetric:
            bound = max(abs(low), abs(high))
            low, high = -bound, bound
        if margin_fraction > 0.0:
            span = high - low
            low -= span * margin_fraction
            high += span * margin_fraction
        return low, high

    if axis in ("x", "both"):
        xlim = merged_limits("get_xlim")
        for ax in axis_list:
            ax.set_xlim(*xlim)
    if axis in ("y", "both"):
        ylim = merged_limits("get_ylim")
        for ax in axis_list:
            ax.set_ylim(*ylim)


def add_panel_labels(
    axes: Iterable[Axes],
    *,
    labels: Sequence[str] | None = None,
    x: float = -0.12,
    y: float = 1.04,
    fontweight: str = "bold",
    fontsize: float | None = None,
    style: Literal["parentheses", "bare"] = "parentheses",
) -> list[Text]:
    """Add consistent panel labels such as (a), (b), and (c)."""
    axis_list = list(axes)
    if labels is None:
        letters = [chr(ord("a") + i) for i in range(len(axis_list))]
        labels = [f"({letter})" if style == "parentheses" else letter for letter in letters]
    if len(labels) != len(axis_list):
        raise ValueError("labels and axes must have the same length.")

    texts: list[Text] = []
    for ax, label in zip(axis_list, labels):
        texts.append(
            ax.text(
                x,
                y,
                label,
                transform=ax.transAxes,
                ha="left",
                va="bottom",
                fontweight=fontweight,
                fontsize=fontsize,
            )
        )
    return texts


def resize_for_paper(
    fig: Figure,
    *,
    column: ColumnSize = "single",
    aspect: Aspect | float = "golden",
    height: float | None = None,
) -> None:
    """Resize an existing figure to a paper-oriented size."""
    fig.set_size_inches(*get_paper_size(column=column, aspect=aspect, height=height), forward=True)


def polish_axes(
    ax: Axes,
    *,
    xlabel: str | None = None,
    ylabel: str | None = None,
    title: str | None = None,
    xlim: tuple[float, float] | None = None,
    ylim: tuple[float, float] | None = None,
    grid: bool = False,
    grid_style: Literal["subtle", "major", "none"] = "subtle",
    minor_ticks: bool = True,
    tick_direction: Literal["in", "out", "inout"] = "in",
    spine_width: float = 1.2,
    hide_top_spine: bool = False,
    hide_right_spine: bool = False,
) -> Axes:
    """Apply readable journal-style formatting to one Matplotlib axis."""
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)
    if title is not None:
        ax.set_title(title, pad=6)
    if xlim is not None:
        ax.set_xlim(*xlim)
    if ylim is not None:
        ax.set_ylim(*ylim)

    if minor_ticks:
        ax.minorticks_on()

    ax.tick_params(
        which="both",
        direction=tick_direction,
        top=not hide_top_spine,
        right=not hide_right_spine,
    )
    ax.tick_params(which="major", length=5.5, width=1.2)
    ax.tick_params(which="minor", length=3.0, width=1.0)

    for side, spine in ax.spines.items():
        spine.set_linewidth(spine_width)
        if side == "top" and hide_top_spine:
            spine.set_visible(False)
        if side == "right" and hide_right_spine:
            spine.set_visible(False)

    if grid and grid_style != "none":
        alpha = 0.22 if grid_style == "subtle" else 0.35
        ax.grid(True, which="major", color="0.75", linewidth=0.8, alpha=alpha)
        ax.grid(True, which="minor", color="0.88", linewidth=0.5, alpha=alpha * 0.7)
    else:
        ax.grid(False)

    return ax


def style_legend(
    ax: Axes,
    *,
    loc: str = "best",
    ncol: int = 1,
    frameon: bool = True,
    outside: Literal[False, "right", "top"] = False,
    title: str | None = None,
) -> mpl.legend.Legend | None:
    """Create or restyle a readable publication legend."""
    handles, labels = ax.get_legend_handles_labels()
    if not handles:
        return None

    kwargs: dict[str, object] = {
        "loc": loc,
        "ncol": ncol,
        "frameon": frameon,
        "title": title,
    }
    if outside == "right":
        kwargs.update({"loc": "center left", "bbox_to_anchor": (1.02, 0.5), "borderaxespad": 0.0})
    elif outside == "top":
        kwargs.update({"loc": "lower center", "bbox_to_anchor": (0.5, 1.02), "borderaxespad": 0.0})

    legend = ax.legend(**kwargs)
    if legend is not None and frameon:
        frame = legend.get_frame()
        frame.set_linewidth(0.8)
        frame.set_edgecolor("0.3")
        frame.set_facecolor("white")
    return legend


def apply_publication_style(
    fig: Figure | None = None,
    axes: Axes | Iterable[Axes] | None = None,
    *,
    font_scale: float = 1.0,
    column: ColumnSize | None = None,
    aspect: Aspect | float = "golden",
    palette: Palette = "colorblind",
    grid: bool = False,
    legends: bool = True,
    marker_edges: bool = True,
) -> None:
    """Apply publication styling to an existing figure and axes."""
    if fig is None:
        fig = plt.gcf()
    if column is not None:
        resize_for_paper(fig, column=column, aspect=aspect)

    mpl.rcParams.update(_scaled_sizes(font_scale))
    for ax in _iter_axes(fig, axes):
        set_distinguishable_cycle(ax, palette=palette)
        polish_axes(ax, grid=grid)
        if marker_edges:
            apply_marker_edges(ax)
        if legends:
            style_legend(ax)

    fig.patch.set_facecolor("white")


def save_publication_figure(
    fig: Figure,
    name: str | Path,
    *,
    formats: Sequence[str] = ("pdf", "svg", "png"),
    dpi: int = 300,
    bbox_inches: str = "tight",
    transparent: bool = False,
    close: bool = False,
) -> list[Path]:
    """Save a figure in publication-oriented vector and raster formats."""
    base = Path(name)
    base.parent.mkdir(parents=True, exist_ok=True)

    written: list[Path] = []
    for fmt in formats:
        suffix = fmt.lower().lstrip(".")
        path = base.with_suffix(f".{suffix}")
        fig.savefig(path, dpi=dpi, bbox_inches=bbox_inches, transparent=transparent)
        written.append(path)

    if close:
        plt.close(fig)
    return written


def compose_caption(
    *,
    what: str,
    axes: str,
    encodings: str | None = None,
    message: str | None = None,
    conditions: str | None = None,
) -> str:
    """Build a compact, self-contained scientific figure caption."""
    parts = [what.rstrip(".") + ".", axes.rstrip(".") + "."]
    if encodings:
        parts.append(encodings.rstrip(".") + ".")
    if conditions:
        parts.append(conditions.rstrip(".") + ".")
    if message:
        parts.append(message.rstrip(".") + ".")
    return " ".join(parts)


def figure_review_checklist() -> tuple[str, ...]:
    """Return a concise checklist for reviewing publication-quality figures."""
    return FIGURE_REVIEW_CHECKLIST
