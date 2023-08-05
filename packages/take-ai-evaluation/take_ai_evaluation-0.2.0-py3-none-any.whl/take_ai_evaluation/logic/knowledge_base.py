import typing as tp

import pandas as pd
import numpy as np

from .intent import Intent

DF = pd.DataFrame
DictOrDataframe = tp.Union[tp.Dict, DF]


class KnowledgeBase:
    """Wraps methods for calculating insights regarding the quality of the Knowledge Base.

    Also grants access to intent level insights.

    Attributes
    ----------
    analysed_base : str
        Analysed base file dataframe.
    labels: list of str
        List of unique intent labels in the knowledge base.
    y_true: list of str
        List of true intent labels in the knowledge base.
    y_pred: list of str
        List of predicted intent labels in the knowledge base.
    intents: dict of Intent
        Dictionary of all intents in the knowledge base.
    all_vs_all_confusion_matrix: pandas.DataFrame
        All vs ALL confusion matrix of the knowledge base.

    Methods
    -------
    get_intent(intent)
        Provides a intent.
    get_best_intent(metric)
        Provides best intent based on a metric.
    get_worst_intent(metric)
        Provides worst intent based on a metric.
    get_classification_report(as_dataframe)
        Provides metrics classification report.
    """

    def __init__(self, analysed_base: DF, intent_col: str, predict_col: str) -> None:
        """
        Parameters
        ----------
        analysed_base: pandas.DataFrame
            Analysed base file dataframe.
        intent_col : str
            Column containing the original intents in your knowledge base.
        predict_col : str
            Column containing the predicted intents in your knowledge base.
        """
        self.init_attributes(analysed_base=analysed_base, intent_col=intent_col, predict_col=predict_col)

    @property
    def analysed_base(self) -> DF:
        """Provides `analysed_base`.

        Returns
        -------
        analysed_base : pandas.DataFrame
            Dataframe object containing the knowledge base.
        """
        return self._analysed_base

    @analysed_base.setter
    def analysed_base(self, analysed_base: DF) -> None:
        """Raises an error when trying to set `analysed_base`.

        Please, do NOT use this method. Use `init_attributes` instead.

        Parameters
        ----------
        analysed_base : pandas.DataFrame
            Dataframe object, can be a file to be read.

        Raises
        ------
        AttributeError
            If `analysed_base` is trying to be set.
        """
        raise AttributeError('Please use `init_attributes` to change `analysed_base` dataset.')

    def init_attributes(self, analysed_base: DF, intent_col: str, predict_col: str) -> None:
        """Initiates all attributes for a given `analysed_base` dataset.

        Parameters
        ----------
        analysed_base: pandas.DataFrame
            Analysed base file dataframe.
        intent_col : str
            Column containing the original intents in your knowledge base.
        predict_col : str
            Column containing the predicted intents in your knowledge base.
        """
        self._analysed_base = analysed_base

        self.labels = self._analysed_base[intent_col].unique()

        self.y_true = self._analysed_base[intent_col]
        self.y_pred = self._analysed_base[predict_col]

        self.intents = {}
        self.classification_report = {}

        self.__calculate_all_vs_all_confusion_matrix()

    def __create_empty_all_vs_all_matrix(self) -> DF:
        """Initializes a ALL vs ALL (multilabel) confusion matrix filled with zeros.

        Returns
        -------
        matrix : pandas.DataFrame:
            Zero filled 2d dataframe with the size of the label count.
        """
        label_count = self.labels.size

        return pd.DataFrame(data=np.zeros((label_count, label_count)),
                            index=self.labels,
                            columns=self.labels)

    def __calculate_all_vs_all_confusion_matrix(self) -> None:
        """Calculates the confusion matrix for this knowledge base.
        """
        confusion_matrix = self.__create_empty_all_vs_all_matrix()

        for i in range(len(self.y_true)):
            confusion_matrix[self.y_true[i]][self.y_pred[i]] += 1.

        self.all_vs_all_confusion_matrix = confusion_matrix

    def get_classification_report(self) -> DictOrDataframe:
        """Provides classification metrics report.

        Returns
        -------
        classification_report : dict of dict or str.
            Classification metrics report.

        Raises
        ------
        ZeroDivisionError
            If during intent's metrics calculation the denominator evaluates to zero.
        """
        if not self.classification_report:
            self.classification_report = self.__calculate_classification_report()

        return self.classification_report

    def __calculate_classification_report(self) -> tp.Dict:
        """Calculates metrics classification report.

        Returns
        -------
        classification_report : dict of dict or str.
            Metrics classification report.

        Raises
        ------
        ZeroDivisionError
            If during intent's metrics calculation the denominator evaluates to zero.
        """
        classification_report = {label: {} for label in self.labels}

        total = self.all_vs_all_confusion_matrix.sum().sum()
        total_tp = 0.

        for label in self.labels:
            intent = self.get_intent(intent=label)

            total_tp += intent.tp
            classification_report[label]['precision'] = intent.precision
            classification_report[label]['recall'] = intent.recall
            classification_report[label]['f1-score'] = intent.f1

        classification_report['accuracy'] = total_tp / total

        return classification_report

    def get_intent(self, intent: str) -> Intent:
        """Provides intent.

        Parameters
        ----------
        intent : str
            Label of the intent to be retrieved.

        Returns
        -------
        intent : Intent
            Requested intent.

        Raises
        ------
        ZeroDivisionError
            If during intent's metrics calculation the denominator evaluates to zero.
        """
        if intent not in self.intents:
            self.intents[intent] = Intent(label=intent,
                                          all_vs_all_confusion_matrix=self.all_vs_all_confusion_matrix)

        return self.intents[intent]

    def get_best_intent(self, metric: str = 'accuracy') -> tp.Tuple[str, float]:
        """Provides best intent based on a metric.

        Parameters
        ----------
        metric : str
            Metric for which the value will be retrieved.
            Can be either of "accuracy", "precision", "recall" or "f1".

        Returns
        -------
        intent : tuple of str and float
            Tuple containing intent name and metric value.

        Raises
        ------
        KeyError
            If `metric` is not any of the expected ones.
        ZeroDivisionError
            If during intent's metrics calculation the denominator evaluates to zero.
        """
        return self.__sort_metrics(metric=metric)[-1]

    def get_worst_intent(self, metric: str = 'accuracy') -> tp.Tuple[str, float]:
        """Provides worst intent based on a metric.

        Parameters
        ----------
        metric : str
            Metric for which the value will be retrieved.
            Can be either of "accuracy", "precision", "recall" or "f1".

        Returns
        -------
        intent : tuple of str and float
            Tuple containing intent name and metric value.

        Raises
        ------
        KeyError
            If `metric` is not any of the expected ones.
        ZeroDivisionError
            If during intent's metrics calculation the denominator evaluates to zero.
        """
        return self.__sort_metrics(metric)[0]

    def __sort_metrics(self, metric: str = 'accuracy') -> tp.List[tp.Tuple]:
        """Sorts in ascending order a list of intents and its values based on a metric.

        Parameters
        ----------
        metric : str
            Metric for which the value will be retrieved.
            Can be either of "accuracy", "precision", "recall" or "f1".

        Returns
        -------
        metrics : list of tuple.
            Sorted list

        Raises
        ------
        KeyError
            If `metric` is not any of the expected ones.
        ZeroDivisionError
            If during intent's metrics calculation the denominator evaluates to zero.
        """
        metrics = {}

        for label in self.labels:
            intent = self.get_intent(intent=label)
            metrics[intent.label] = intent.get_metric(metric=metric)

        sorted_metrics = sorted(metrics.items(), key=lambda item: item[1])

        return sorted_metrics
