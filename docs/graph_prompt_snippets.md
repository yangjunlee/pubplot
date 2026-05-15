# Graph Prompt Snippets

These snippets translate manuscript-writing guidance into practical prompts for generating or revising scientific figures. They are intended for physics and materials-science plots where the figure should support the paper's scientific argument, not merely look decorative.

## Integrated Prompt

Improve this graph for use in a physics/materials-science paper.

Make the figure publication-quality and consistent with high-impact journal standards. The figure should be understandable from the figure and caption alone.

Keep the data unchanged. Improve only the visual presentation.

Apply the following:

- use one consistent font family, preferably Arial or a clean equivalent;
- make all text readable at the final printed manuscript size;
- use consistent capitalization, avoiding unnecessary title case;
- include clear axis labels with units;
- use correct scientific formatting, including spaces between numbers and units and proper minus signs;
- use consistent panel labels and panel-label positions;
- if panels compare the same quantity, match axis scales and tick intervals;
- distinguish multiple datasets using both color and marker or line style, not color alone;
- use refined, colorblind-aware colors rather than harsh default colors;
- use marker edge outlines when they improve visibility;
- format legends with the visual symbol first and the explanatory label second;
- place legends so they do not cover important data;
- use annotations and arrows only when they clarify the scientific message;
- make arrow directions intuitive, with the label pointing toward the relevant object or feature;
- reduce clutter and remove unnecessary decorative elements;
- optimize spacing so that labels, ticks, and legends are not clipped;
- save the final figure as PDF and SVG, with optional high-DPI PNG.

Also provide a short, self-contained caption that explains what is plotted, what the colors or markers mean, and what the main scientific message is.

## Figure Quality Rules

1. The figure should be understandable without heavy reliance on the main text.
2. The visual flow should follow the logical order of the paper, not the historical order of the research.
3. All visual choices should be intentional: font, size, color, marker, line width, axis scale, legend, annotation, and panel label.
4. Use one consistent font family throughout the figure.
5. Tune font sizes for the final printed or submitted figure size.
6. Use consistent panel-label style and placement.
7. When comparing the same physical quantity, match axis scales and tick intervals.
8. Use both color and marker or line style to distinguish multiple datasets.
9. Avoid relying only on color.
10. Use marker edge outlines when they improve visual distinction.
11. Format legends in the conventional symbol-first style.
12. Use refined, high-impact-paper-like colors rather than harsh default colors.
13. Use clear axis labels with units.
14. Use correct number-unit spacing, mathematical minus signs, and conservative capitalization.
15. Keep captions concise but self-contained.
16. Save figures in vector formats such as PDF or SVG, with optional high-DPI PNG.
17. Do not change the data or scientific meaning while improving the figure.

## Review Checklist

Review this figure as if you are a journal referee and scientific editor.

Check the following:

1. Can the main message be understood from the figure alone?
2. Are the axis labels scientifically precise and complete?
3. Are units included and formatted correctly?
4. Are tick labels readable at final publication size?
5. Are the font family and font sizes consistent?
6. Are panel labels consistent in style and position?
7. If panels compare the same quantity, are axis scales matched?
8. Are colors and markers distinguishable, including in grayscale?
9. Does the legend use symbol-first formatting?
10. Does the legend avoid covering important data?
11. Are annotations and arrows necessary and intuitive?
12. Are line widths, marker sizes, and spine widths suitable for print?
13. Is the caption self-contained?
14. Are there any unnecessary decorative elements?
15. Does the figure follow the logical order of the paper rather than the historical order of the research?

Suggest concrete changes rather than vague comments.

## Plot-Specific Prompts

### Scatter Comparison

Create a publication-quality scatter comparison plot.

- If x and y represent the same physical quantity or comparable quantities, use equal or matched axis limits.
- Add a `y = x` reference line when appropriate.
- Use the same scale on both axes if the purpose is direct comparison.
- Use density coloring only if it clarifies point concentration.
- Use a colorbar with a clear label and readable tick labels.
- Use distinct markers or marker edge styling for different groups.
- Avoid misleading aspect ratios.
- Include units in both axis labels.
- Make the main deviation, agreement, or trend immediately visible.

### Line Plot / Parameter Sweep

Create a publication-quality line plot for multiple parameter values.

- Distinguish curves using both color and line style or marker style.
- Use sufficiently thick lines for print readability.
- Do not rely only on color differences.
- Use a concise legend with symbol or line sample first, followed by the label.
- Use physically meaningful parameter labels and units.
- Order legend entries logically, for example by increasing parameter value.
- Use annotations only for key regimes or transitions.
- Avoid clutter if there are many curves; consider direct labeling or grouping.

### DOS / PDOS

Create a publication-quality DOS/PDOS figure for a physics or materials-science paper.

- Set the Fermi level as a clear reference, usually `E - E_F = 0 eV`.
- Add a vertical reference line at the Fermi level if the energy axis is horizontal.
- Use clear orbital or atomic labels in the legend.
- Distinguish orbital contributions using both color and line style when needed.
- Avoid excessive filling opacity that hides overlapping contributions.
- Use consistent energy limits across related panels.
- Include units for energy and density of states.
- Use one font family and readable tick labels.
- Make the physical interpretation clear, for example band gap, dominant orbital character, or hybridization.

### Band Structure

Create a publication-quality band-structure figure.

- Align the energy zero to the Fermi level or valence-band maximum, and state this clearly in the axis label.
- Use a horizontal reference line at zero energy.
- Label high-symmetry k-points clearly.
- Use vertical guide lines at high-symmetry points.
- Keep line widths readable but not visually heavy.
- Use consistent energy ranges across related band-structure panels.
- If comparing methods or materials, use matched axes and consistent colors or line styles.
- Avoid unnecessary legends if direct labeling or panel captions are clearer.

### Heatmap / Contour

Create a publication-quality heatmap or contour plot.

- Use a scientifically appropriate colormap.
- Avoid rainbow colormaps unless there is a specific reason.
- Include a clearly labeled colorbar with units.
- Use readable colorbar tick labels.
- Make the color scale comparable across panels if the panels show the same quantity.
- State whether the color scale is linear, logarithmic, normalized, or clipped.
- Avoid overplotting text or markers that obscure important color variation.
- Use annotations only for key regions or boundaries.

## Negative Prompt

Do not:

- use tiny default Matplotlib fonts;
- mix multiple font families;
- use inconsistent panel labels;
- compare the same quantity with mismatched axes unless explicitly justified;
- distinguish datasets by color alone;
- use legends that cover important data;
- place verbal descriptions before visual legend symbols;
- use harsh default primary colors when better publication colors are available;
- omit units from axis labels;
- use incorrect spacing between numbers and units;
- use hyphen instead of mathematical minus signs in labels;
- use unnecessary title-case capitalization;
- use decorative arrows or excessive annotations;
- overload a main-text figure with SI-level details;
- save only a low-resolution PNG;
- alter the data or scientific meaning while improving the figure.
