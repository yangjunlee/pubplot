"""Publication-quality Matplotlib utilities for scientific figures."""

from . import presets
from .style import (
    add_panel_labels,
    apply_publication_style,
    apply_marker_edges,
    compose_caption,
    emphasize_zero_axes,
    figure_review_checklist,
    get_paper_size,
    match_axis_limits,
    polish_axes,
    publication_style,
    resize_for_paper,
    save_publication_figure,
    set_distinguishable_cycle,
    style_legend,
)

__all__ = [
    "add_panel_labels",
    "apply_publication_style",
    "apply_marker_edges",
    "compose_caption",
    "emphasize_zero_axes",
    "figure_review_checklist",
    "get_paper_size",
    "match_axis_limits",
    "polish_axes",
    "publication_style",
    "presets",
    "resize_for_paper",
    "save_publication_figure",
    "set_distinguishable_cycle",
    "style_legend",
]
