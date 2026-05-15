# pubplot

`pubplot` is a small Python utility for turning ordinary Matplotlib figures into publication-quality scientific figures. It focuses on readable fonts, clean axes, distinguishable curves, journal-style sizing, and vector output suitable for physics and materials-science papers.

The package does not change the plotted data. It only improves visual presentation.

The style rules are based on manuscript-writing principles: a figure should be understandable from the figure and caption alone, visual choices should follow the paper's logical argument, and final exported text must remain readable at manuscript size.

## Goals

- Make all figure text large and consistent.
- Improve axis labels, tick labels, spines, grids, and legends.
- Use colorblind-friendly and grayscale-aware color/line cycles.
- Resize figures for single-column, double-column, square, or wide paper layouts.
- Save crisp PDF/SVG vector files with optional high-DPI PNG previews.
- Provide presets for common scientific plots such as DOS, PDOS, band structures, convergence plots, and heatmaps.
- Support panel labels, matched axis scales, marker edge outlines, and caption/checklist helpers.

## Installation

From this repository:

```bash
python3 -m pip install -e .
```

For tests:

```bash
python3 -m pip install -e ".[test]"
```

## Quick Start

```python
import numpy as np
import matplotlib.pyplot as plt
import pubplot as pp

x = np.linspace(0.0, 2.0 * np.pi, 400)

with pp.publication_style(font_scale=1.2, column="single"):
    fig, ax = plt.subplots()
    ax.plot(x, np.sin(x), label=r"$\sin x$")
    ax.plot(x, np.cos(x), label=r"$\cos x$")

    pp.polish_axes(
        ax,
        xlabel=r"$x$ (rad)",
        ylabel="Amplitude",
        title="Trigonometric functions",
        grid=False,
    )
    pp.emphasize_zero_axes(ax, y=True)
    pp.style_legend(ax, outside="top", ncol=2, frameon=False)
    pp.save_publication_figure(fig, "figures/trig_demo")
```

This writes:

- `figures/trig_demo.pdf`
- `figures/trig_demo.svg`
- `figures/trig_demo.png`

## Main API

### `publication_style(...)`

Context manager that sets Matplotlib `rcParams` for paper-quality scientific plots.

```python
with pp.publication_style(font_scale=1.2, column="single"):
    ...
```

Useful options:

- `font_scale`: scales titles, labels, ticks, legends, and annotations.
- `column`: `"single"`, `"double"`, `"square"`, or `"wide"`.
- `palette`: `"colorblind"`, `"high_contrast"`, `"grayscale"`, or `"journal"`.
- `font_family`: `"serif"` by default.
- `use_latex`: optional external LaTeX rendering.

### `polish_axes(ax, ...)`

Applies publication-style formatting to one axis:

- larger labels and tick labels
- inward ticks
- optional minor ticks
- controlled spine width
- subtle grid styling
- optional axis labels, title, and limits

### `style_legend(ax, ...)`

Formats legends with readable font size, clean spacing, and a light frame.

### `set_distinguishable_cycle(ax=None, ...)`

Applies a color/line/marker cycle designed to keep multiple curves distinguishable.

### `add_panel_labels(axes, ...)`

Adds consistent panel labels such as `(a)`, `(b)`, and `(c)` at the same relative position in every subplot.

### `match_axis_limits(axes, ...)`

Matches axis limits across panels that compare the same physical quantity.

### `apply_marker_edges(ax, ...)`

Adds dark marker outlines to line markers and scatter markers for print and grayscale readability.

### `emphasize_zero_axes(ax, ...)`

Adds clean reference lines at `x = 0` and/or `y = 0` without drawing an internal grid.

### `compose_caption(...)`

Builds a compact, self-contained caption from what is plotted, axis meanings, visual encodings, conditions, and the main scientific message.

### `resize_for_paper(fig, column=...)`

Sets figure dimensions using common paper-oriented widths.

### `save_publication_figure(fig, name, ...)`

Saves vector output by default:

```python
pp.save_publication_figure(fig, "figures/result", formats=("pdf", "svg", "png"))
```

## Scientific Presets

The `pubplot.presets` module includes targeted helpers:

- `style_dos_plot(ax)`: DOS/PDOS-style energy plots with a Fermi-level reference line.
- `style_band_structure(ax)`: band-structure plots with high-symmetry k-point labels.
- `style_convergence_plot(ax)`: convergence studies with optional tolerance lines.
- `style_heatmap(ax, cbar=...)`: heatmaps with readable colorbar labels.

Example:

```python
pp.presets.style_dos_plot(
    ax,
    energy_axis="x",
    fermi_level=0.0,
    xlabel=r"$E - E_F$ (eV)",
    ylabel="DOS (states/eV)",
)
```

## Example

Run:

```bash
MPLBACKEND=Agg MPLCONFIGDIR=.mplconfig PYTHONPATH=src python3 -m pubplot.cli --output figures/example
```

The command creates a multi-curve scientific demo figure in PDF, SVG, and PNG formats.

## Testing

```bash
MPLBACKEND=Agg MPLCONFIGDIR=.mplconfig python3 -m pytest
```

## Design Notes

The defaults are intentionally conservative:

- white background
- visible black spines
- inward ticks
- large labels and ticks
- subtle optional grid
- vector-first saving
- sans-serif font family by default, with Arial/Helvetica/DejaVu Sans fallback
- color plus line-style cycling by default

Numerical values, units, data arrays, and physical meaning are left unchanged. If a project needs domain-specific conventions, add a small preset rather than changing global behavior.

Additional graph prompt snippets and review rules are stored in [docs/graph_prompt_snippets.md](docs/graph_prompt_snippets.md).
