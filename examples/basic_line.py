"""Basic pubplot usage example."""

import numpy as np
import matplotlib.pyplot as plt

import pubplot as pp


def main() -> None:
    x = np.linspace(0.0, 2.0 * np.pi, 400)

    with pp.publication_style(font_scale=1.2, column="single"):
        fig, ax = plt.subplots()
        ax.plot(x, np.sin(x), label=r"$\sin x$")
        ax.plot(x, np.cos(x), label=r"$\cos x$")
        pp.polish_axes(ax, xlabel=r"$x$ (rad)", ylabel="Amplitude", grid=True)
        pp.style_legend(ax)
        pp.save_publication_figure(fig, "figures/basic_line")


if __name__ == "__main__":
    main()
