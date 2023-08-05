import pandas as pd
import seaborn as sns
import matplotlib

from take_ai_evaluation.logic import normalize_confusion_matrix

DF = pd.DataFrame
AX = matplotlib.axes.Axes


def plot_confusion_matrix(confusion_matrix: DF,
                          title: str,
                          xlabel: str = '',
                          ylabel: str = '',
                          normalize: bool = False) -> AX:
    """Provides the confusion matrix for a knowledge base.

    Parameters
    ----------
    confusion_matrix : pandas.DataFrame
        Confusion matrix to be plotted.
    title : str
        Title for the output graph.
    xlabel : str, optional
        X axis label for the output graph (default is '').
    ylabel : str, optional
        Y axis label for the output graph (default is '').
    normalize : bool, optional
        If True, return output normalized using L1 normalization (default is false).

    Returns
    -------
    ax : matplotlib Axes
        Axes object with the heatmap.
    """
    if normalize:
        confusion_matrix = normalize_confusion_matrix(confusion_matrix=confusion_matrix)

    return _plot_confusion_matrix(confusion_matrix=confusion_matrix, title=title, xlabel=xlabel, ylabel=ylabel)


def _plot_confusion_matrix(confusion_matrix: pd.DataFrame, title: str, xlabel: str, ylabel: str) -> AX:
    """Provides the confusion matrix for a knowledge base.

    Parameters
    ----------
    confusion_matrix : pandas.DataFrame
        Confusion matrix to be plotted.
    title : str
        Title for the output graph.
    xlabel : str, optional
        X axis label for the output graph (default is '').
    ylabel : str, optional
        Y axis label for the output graph (default is '').

    Returns
    -------
    ax : matplotlib Axes
        Axes object with the heatmap.
    """
    ax = sns.heatmap(data=confusion_matrix, annot=True, linewidths=.5)

    ax.set_title(label=title)
    ax.set_xlabel(xlabel=xlabel)
    ax.set_ylabel(ylabel=ylabel)

    return ax
