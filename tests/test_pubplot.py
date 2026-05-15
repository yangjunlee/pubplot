import os

os.environ.setdefault("MPLBACKEND", "Agg")

import matplotlib.pyplot as plt
import numpy as np

import pubplot as pp
from pubplot import presets


def test_get_paper_size_single_golden():
    width, height = pp.get_paper_size("single", "golden")
    assert width == 3.45
    assert 2.12 < height < 2.14


def test_polish_axes_and_legend():
    with pp.publication_style(font_scale=1.2):
        fig, ax = plt.subplots()
        ax.plot([0, 1], [0, 1], label="data")
        pp.polish_axes(ax, xlabel="x", ylabel="y", grid=True)
        legend = pp.style_legend(ax)

    assert ax.get_xlabel() == "x"
    assert ax.get_ylabel() == "y"
    assert legend is not None
    plt.close(fig)


def test_outside_top_legend():
    with pp.publication_style():
        fig, ax = plt.subplots()
        ax.plot([0, 1], [0, 1], label="first")
        ax.plot([0, 1], [1, 0], label="second")
        legend = pp.style_legend(ax, outside="top", ncol=2, frameon=False)

    assert legend is not None
    assert len(legend.get_texts()) == 2
    plt.close(fig)


def test_save_publication_figure(tmp_path):
    with pp.publication_style():
        fig, ax = plt.subplots()
        ax.plot([0, 1], [1, 0])
        written = pp.save_publication_figure(fig, tmp_path / "figure", formats=("pdf", "svg", "png"))

    assert {path.suffix for path in written} == {".pdf", ".svg", ".png"}
    assert all(path.exists() and path.stat().st_size > 0 for path in written)
    plt.close(fig)


def test_dos_preset_adds_fermi_line():
    with pp.publication_style():
        fig, ax = plt.subplots()
        energy = np.linspace(-2.0, 2.0, 50)
        ax.plot(energy, energy**2, label="DOS")
        presets.style_dos_plot(ax)

    assert ax.get_xlabel() == r"$E - E_F$ (eV)"
    assert len(ax.lines) == 2
    plt.close(fig)


def test_band_structure_labels_validation():
    with pp.publication_style():
        fig, ax = plt.subplots()
        try:
            presets.style_band_structure(ax, kpoints=[0.0, 1.0], labels=[r"$\Gamma$"])
        except ValueError as exc:
            assert "same length" in str(exc)
        else:
            raise AssertionError("Expected mismatched labels to raise ValueError.")
    plt.close(fig)


def test_all_palettes_build_valid_cycles():
    for palette in ("colorblind", "high_contrast", "grayscale", "journal"):
        with pp.publication_style(palette=palette):
            fig, ax = plt.subplots()
            pp.set_distinguishable_cycle(ax, palette=palette, use_markers=True)
            ax.plot([0, 1], [0, 1])
        plt.close(fig)


def test_presets_module_is_exposed_from_top_level():
    assert pp.presets is presets


def test_panel_labels_and_matched_axis_limits():
    with pp.publication_style():
        fig, axes = plt.subplots(1, 2)
        axes[0].plot([0, 1], [0, 2])
        axes[1].plot([0, 2], [-1, 1])
        labels = pp.add_panel_labels(axes)
        pp.match_axis_limits(axes, axis="both")

    assert [text.get_text() for text in labels] == ["(a)", "(b)"]
    assert axes[0].get_xlim() == axes[1].get_xlim()
    assert axes[0].get_ylim() == axes[1].get_ylim()
    plt.close(fig)


def test_marker_edges_apply_to_scatter_and_lines():
    with pp.publication_style():
        fig, ax = plt.subplots()
        line = ax.plot([0, 1], [0, 1], marker="o")[0]
        scatter = ax.scatter([0.5], [0.5], marker="s")
        pp.apply_marker_edges(ax, edgecolor="black", linewidth=1.1)

    assert line.get_markeredgecolor() == "black"
    assert line.get_markeredgewidth() == 1.1
    assert scatter.get_linewidths()[0] == 1.1
    plt.close(fig)


def test_emphasize_zero_axes_adds_reference_lines():
    with pp.publication_style():
        fig, ax = plt.subplots()
        pp.emphasize_zero_axes(ax, x=True, y=True)

    assert len(ax.lines) == 2
    assert all(line.get_zorder() == 0.5 for line in ax.lines)
    plt.close(fig)


def test_caption_and_checklist_helpers():
    caption = pp.compose_caption(
        what="Comparison of calculated formation energies",
        axes="The x-axis shows composition and the y-axis shows formation energy (eV/atom)",
        encodings="Colors and markers distinguish calculation methods",
        message="The convex-hull candidates are visually separated from unstable phases",
    )

    assert "formation energy" in caption
    assert "Colors and markers" in caption
    assert any("axis labels" in item for item in pp.figure_review_checklist())
