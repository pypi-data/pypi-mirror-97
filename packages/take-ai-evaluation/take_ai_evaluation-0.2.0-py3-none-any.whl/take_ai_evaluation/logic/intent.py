import pandas as pd

DF = pd.DataFrame


class Intent:
    """Wraps methods for calculating insights regarding the quality of the intent.

    Attributes
    ----------
    label : str
        Intent's label (name).
    tp: float
        Intent's true positive predictions.
    fn: float
        Intent's false negative predictions.
    fp: float
        Intent's false positive predictions.
    tn: float
        Intent's true negative predictions.
    one_vs_all_confusion_matrix: pandas.DataFrame
        ONE vs ALL confusion matrix of the intent.
    metrics_mapper : dict
        Dict that maps accuracy, precision, recall and f1 values for a intent.
    accuracy: float
        Accuracy score for a intent.
    precision : float
        Precision score for a intent.
    recall : float
        Recall score for a intent.
    f1 : float
        F1 score, also known as balanced F-score or F-measure, for a intent.

    Methods
    -------
    get_metric(metric)
        Provides the calculated value for a specific metric.

    Raises
    ------
    ZeroDivisionError
        If during metrics calculation the denominator evaluates to zero.
    """

    def __init__(self, label: str, all_vs_all_confusion_matrix: DF) -> None:
        """
        Parameters
        ----------
        label : str
            Label of the intent to be retrieved.
        all_vs_all_confusion_matrix : pandas.DataFrame
            ALL vs ALL confusion matrix.
        """
        self.label = label

        self.__make_one_vs_all_confusion_matrix(all_vs_all_confusion_matrix=all_vs_all_confusion_matrix)
        self.__make_metrics_mapper()

    def __create_one_vs_all_confusion_matrix(self) -> DF:
        """Creates a ONE vs ALL (multilabel) confusion matrix filled with it's results.

        Returns
        -------
        matrix : pandas.DataFrame
            Metrics filled 2d dataframe with the size of 2 by 2.
        """
        data = ((self.tp, self.fn), (self.fp, self.tn))

        return pd.DataFrame(data=data, columns=['Positive', 'Negative'], index=['Positive', 'Negative'])

    def __calculate_one_vs_all_confusion_matrix(self, all_vs_all_confusion_matrix: DF) -> None:
        """Calculates the confusion matrix (TP, FP, FN, TN) for a intent.

        Parameters
        ----------
        all_vs_all_confusion_matrix : pandas.DataFrame
            ALL vs ALL confusion matrix.
        """
        n = all_vs_all_confusion_matrix.sum().sum()
        self.tp = all_vs_all_confusion_matrix[self.label][self.label]
        self.fp = all_vs_all_confusion_matrix[self.label].sum() - self.tp
        self.fn = all_vs_all_confusion_matrix.loc[self.label].sum() - self.tp
        self.tn = n - (self.tp + self.fn + self.fp)

    def __make_one_vs_all_confusion_matrix(self, all_vs_all_confusion_matrix: DF) -> None:
        """Generates and assigns a confusion matrix for a intent.

        Parameters
        ----------
        all_vs_all_confusion_matrix : pandas.DataFrame
            ALL vs ALL confusion matrix.
        """
        self.__calculate_one_vs_all_confusion_matrix(all_vs_all_confusion_matrix=all_vs_all_confusion_matrix)
        self.one_vs_all_confusion_matrix = self.__create_one_vs_all_confusion_matrix()

    def __calculate_metrics(self) -> None:
        """Calculates accuracy, precision, recall and f1 for a intent.

        Raises
        ------
        ZeroDivisionError
            If during metrics calculation the denominator evaluates to zero.
        """
        self.__calculate_accuracy()
        self.__calculate_precision()
        self.__calculate_recall()
        self.__calculate_f1()

    def __make_metrics_mapper(self) -> None:
        """Calculates and maps accuracy, precision, recall and f1 for a intent.

        Raises
        ------
        ZeroDivisionError
            If during metrics calculation the denominator evaluates to zero.
        """
        self.__calculate_metrics()

        self.metrics_mapper = {'accuracy': self.accuracy,
                               'precision': self.precision,
                               'recall': self.recall,
                               'f1': self.f1}

    def __calculate_accuracy(self) -> None:
        """Calculates the accuracy score for a intent.

        The accuracy is the ratio `(tp + fn) / (tp + fn + tn + fp)`
        where `tp` is the number of true positives, `fn` the number
        of false negatives, `tn` is the number of true negatives
        and `fp` the number of false positives. The accuracy is the
        ability of the instrument to measure the accurate value.
        In other words, it is the closeness of the measured
        value to a standard or true value.

        The best value is 1 and the worst value is 0.

        Raises
        ------
        ZeroDivisionError
            If `(tp + fn + tn + fp)` evaluates to zero.
        """
        nominator = (self.tp + self.fn)
        denominator = (self.tp + self.fn + self.tn + self.fp)

        if denominator > 0:
            self.accuracy = nominator / denominator
        else:
            raise ZeroDivisionError(f"`{self.label}` accuracy denominator cannot be zero.")

    def __calculate_precision(self) -> None:
        """Calculates the precision score for a intent.

        The precision is the ratio `tp / (tp + fp)` where `tp` is
        the number of true positives and `fp` the number of false
        positives. The precision is intuitively the ability of the
        classifier not to label as positive a sample that is negative.

        The best value is 1 and the worst value is 0.

        Raises
        ------
        ZeroDivisionError
            If `(tp + fp)` evaluates to zero.
        """
        denominator = (self.tp + self.fp)

        if denominator > 0:
            self.precision = self.tp / denominator
        else:
            raise ZeroDivisionError(f"`{self.label}` precision denominator cannot be zero.")

    def __calculate_recall(self) -> None:
        """Calculate the recall score for a intent.

        The recall is the ratio `tp / (tp + fn)` where `tp` is
        the number of true positives and `fn` the number of false
        negatives. The recall is intuitively the ability of the
        classifier to find all the positive samples.

        The best value is 1 and the worst value is 0.

        Raises
        ------
        ZeroDivisionError
            If `(tp + fn)` evaluates to zero.
        """
        denominator = (self.tp + self.fn)

        if denominator > 0:
            self.recall = self.tp / denominator
        else:
            raise ZeroDivisionError(f"`{self.label}` recall denominator cannot be zero.")

    def __calculate_f1(self) -> None:
        """Calculates the F1 score, also known as balanced F-score or F-measure, for a intent.

        The F1 score is the ratio `2 * (precision * recall) / (precision + recall)`
        and can be interpreted as a weighted average of the precision
        and recall. The relative contribution of precision and recall
        to the F1 score are equal.

        The best value is 1 and the worst value is 0.

        Raises
        ------
        ZeroDivisionError
            If `(precision + recall)` evaluates to zero.
        """
        nominator = (2 * self.precision * self.recall)
        denominator = (self.precision + self.recall)

        if denominator > 0:
            self.f1 = nominator / denominator
        else:
            raise ZeroDivisionError(f"`{self.label}` F1 denominator cannot be zero.")

    def get_metric(self, metric: str) -> float:
        """Provides the calculated value for a specific metric of a intent.

        Parameters
        ----------
        metric : str
            Metric for which the value will be retrived.
            Can be either of "accuracy", "precision", "recall" or "f1".

        Returns
        -------
        metric : float
            Requested metric's value.

        Raises
        ------
        KeyError
            If `metric` is any of the expected ones.
        """
        return self.metrics_mapper[metric]
