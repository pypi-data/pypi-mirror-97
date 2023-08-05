import pandas as pd
from sklearn.preprocessing import normalize as norm

DF = pd.DataFrame


def normalize_confusion_matrix(confusion_matrix: DF) -> DF:
    """Calculates the normalized confusion matrix using L1 normalization.

    Parameters
    ----------
    confusion_matrix : pandas.DataFrame
        Dataframe containing the original confusion matrix.

    Returns
    -------
    matrix : pandas.DataFrame
        Dataframe containing the normalized confusion matrix.
    """
    return pd.DataFrame(data=norm(confusion_matrix, norm="l1"),
                        index=confusion_matrix.index,
                        columns=confusion_matrix.columns)
