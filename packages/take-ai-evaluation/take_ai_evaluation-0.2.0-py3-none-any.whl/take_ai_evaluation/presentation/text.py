import matplotlib
import matplotlib.patheffects as path_effects
import matplotlib.pyplot as plt

AX = matplotlib.axes.Axes


def plot_text(text: str, title: str, title_size: int = 30) -> AX:
    """Plots a text.

    Parameters
    ----------
    text : str
        Text to be plotted.
    title : str
        Title for the output graph.
    title_size : int, optional
        Title's size (defaults is 30 pixels).

    Returns
    -------
    ax : matplotlib Axes
        Axes object with the text.
    """
    fig, ax = plt.subplots()

    text = fig.text(0.5, 0.5, text, ha='center', va='center', size=title_size * 0.9)
    text.set_path_effects([path_effects.Normal()])

    ax.set_title(title, fontsize=title_size)
    ax.set_axis_off()

    return ax
