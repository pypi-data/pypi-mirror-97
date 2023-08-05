import typing as tp

import pandas as pd
import matplotlib

from take_ai_evaluation.logic import KnowledgeBase, validate_dataframe, validate_parameters, validate_parameter
from take_ai_evaluation.persistence import read_dataframe
from take_ai_evaluation.presentation import plot_confusion_matrix, plot_text

DF = pd.DataFrame
AX = matplotlib.axes.Axes

StrOrDataframe = tp.Union[str, DF]
TupleOrAxes = tp.Union[tp.Tuple, AX]
DictOrDataframe = tp.Union[tp.Dict, DF]


class AiEvaluation:
    """Wraps methods for calling and using the package's visualizations.

    Attributes
    ----------
    intent_col : str
        Column containing the original intents in your knowledge base.
    predict_col: str
        Column containing the original intents in your knowledge base.
    analysed_base: pandas.DataFrame
        Dataframe object containing the knowledge base.
    knowledge_base: KnowledgeBase
        Object that wraps methods for calculating insights regarding the quality of the Knowledge Base.

    Methods
    -------
    init_attributes(analysed_base, sentence_col, intent_col, predict_col, analysed_base_sep)
        Initiates all attributes for a given `analysed_base` dataset.
    get_all_vs_all_confusion_matrix(title, normalize=False)
        Provides the ALL vs ALL confusion matrix.
    get_one_vs_all_confusion_matrix(title, normalize=False)
        Provides the ONE vs ALL confusion matrix.
    get_best_intent(metric='accuracy', as_graph=False)
        Provides best intent based on a metric.
    get_worst_intent(metric='accuracy', as_graph=False)
        Provides worst intent based on a metric.
    get_classification_report(as_dataframe=False)
        Provides classification metrics report.

    Raises
    ------
    TypeError
        If the during `analysed_base` validation any parameter's type or itself does not match the desired type.
    ValueError
        If the during `analysed_base` validation any parameter or itself is empty.
    FileNotFoundError
        If during knowledge base reading `analysed_base` file is not found.
    AttributeError
        If any of the expected columns is not present inside the knowledge base dataframe.
    """

    def __init__(self,
                 analysed_base: StrOrDataframe,
                 sentence_col: str,
                 intent_col: str,
                 predict_col: str,
                 analysed_base_sep: str = '|') -> None:
        """
        Parameters
        ----------
        analysed_base : str | pandas.DataFrame
            Dataframe object, can be a file to be read.
        sentence_col : str
            Column containing the original sentence in your knowledge base.
        intent_col : str
            Column containing the original intents in your knowledge base.
        predict_col : str
            Column containing the predicted intents in your knowledge base.
        analysed_base_sep : str, optional
            CSV separator (default is "|").
        """
        self.init_attributes(analysed_base=analysed_base,
                             sentence_col=sentence_col,
                             intent_col=intent_col,
                             predict_col=predict_col,
                             analysed_base_sep=analysed_base_sep)

    def __validate_params(self,
                          analysed_base: StrOrDataframe,
                          sentence_col: str,
                          intent_col: str,
                          predict_col: str) -> None:
        """Validates parameters' types and values.

        Parameters
        ----------
        analysed_base : str | pandas.DataFrame
            Dataframe object, can be a file to be read.
        sentence_col : str
            Column containing the original sentence in your knowledge base.
        intent_col : str
            Column containing the original intents in your knowledge base.
        predict_col : str
            Column containing the predicted intents in your knowledge base.

        Raises
        ------
        TypeError
            If the parameter's type does not match the desired type.
        ValueError
            If the parameter is empty.
        """
        validate_parameter(param=analysed_base, param_name='analysed_base', target_type=(str, DF))
        validate_parameter(param=sentence_col, param_name='sentence_col', target_type=str)
        validate_parameter(param=intent_col, param_name='intent_col', target_type=str)
        validate_parameter(param=predict_col, param_name='predict_col', target_type=str)

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
    def analysed_base(self, analysed_base: StrOrDataframe) -> None:
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

    def init_attributes(self,
                        analysed_base: StrOrDataframe,
                        sentence_col: str,
                        intent_col: str,
                        predict_col: str,
                        analysed_base_sep: str) -> None:
        """Initiates all attributes for a given `analysed_base` dataset.

        Parameters
        ----------
        analysed_base : str | pandas.DataFrame
            Dataframe object, can be a file to be read.
        sentence_col : str
            Column containing the original sentence in your knowledge base.
        intent_col : str
            Column containing the original intents in your knowledge base.
        predict_col : str
            Column containing the predicted intents in your knowledge base.
        analysed_base_sep : str
            CSV separator.

        Raises
        ------
        TypeError
            If the during `analysed_base` validation any parameter's type or itself does not match the desired type.
        ValueError
            If the during `analysed_base` validation any parameter or itself is empty.
        FileNotFoundError
            If during knowledge base reading `analysed_base` file is not found.
        AttributeError
            If any of the expected columns is not present inside the knowledge base dataframe.
        """
        self.__validate_params(analysed_base=analysed_base,
                               sentence_col=sentence_col,
                               intent_col=intent_col,
                               predict_col=predict_col)

        self.intent_col = intent_col
        self.predict_col = predict_col

        self.__init_analysed_base(analysed_base=analysed_base,
                                  analysed_base_sep=analysed_base_sep,
                                  sentence_col=sentence_col)

        self.__init_knowledge_base()

    def __init_analysed_base(self, analysed_base: StrOrDataframe, analysed_base_sep: str, sentence_col: str) -> None:
        """Reads knowledge base based on `analysed_base`.

        Parameters
        ----------
        analysed_base : str | pandas.DataFrame
            Dataframe object, can be a file to be read.
        analysed_base_sep : str
            CSV separator.
        sentence_col : str
            Column containing the original sentence in your knowledge base.

        Raises
        ------
        TypeError
            If `analysed_base` is not the expected type.
        FileNotFoundError
            If `analysed_base` file is not found.
        ValueError
            If after read `analysed_base` is empty.
        AttributeError
            If during `analysed_base` validation any of the expected columns is not present in it.
        """
        analysed_base = read_dataframe(dataframe=analysed_base, sep=analysed_base_sep)

        columns = [sentence_col, self.intent_col, self.predict_col]
        validate_dataframe(df=analysed_base, columns=columns)

        self._analysed_base = analysed_base

    def __init_knowledge_base(self) -> None:
        """Initializes the knowledge base object after reading it's files.
        """
        self.knowledge_base = KnowledgeBase(analysed_base=self._analysed_base,
                                            intent_col=self.intent_col,
                                            predict_col=self.predict_col)

    def get_all_vs_all_confusion_matrix(self, title: str, normalize: bool = False) -> AX:
        """Provides the ALL vs ALL confusion matrix for a knowledge base.

        Parameters
        ----------
        title : str
            Wanted title for the output graph.
        normalize : bool, optional
            If True, return output normalized using L1 normalization (default is false).

        Returns
        -------
        matrix : matplotlib Axes
            Axes object with the confusion matrix.
        """
        return plot_confusion_matrix(confusion_matrix=self.knowledge_base.all_vs_all_confusion_matrix,
                                     title=title,
                                     xlabel='Predicted label',
                                     ylabel='True label',
                                     normalize=normalize)

    def get_one_vs_all_confusion_matrix(self, intent: str, title: str, normalize: bool = False) -> AX:
        """Provides the ONE vs ALL confusion matrix for a knowledge base and a given intent.

        Parameters
        ----------
        intent : str
            Label of the intent to be retrieved.
        title : str
            Wanted title for the output graph.
        normalize : bool, optional
            If True, return output normalized using L1 normalization (default is false).

        Returns
        -------
        matrix : matplotlib Axes
            Axes object with the confusion matrix.

        Raises
        ------
        ZeroDivisionError
            If during intent's metrics calculation the denominator evaluates to zero.
        """
        intent = self.knowledge_base.get_intent(intent=intent)

        return plot_confusion_matrix(confusion_matrix=intent.one_vs_all_confusion_matrix,
                                     title=title,
                                     xlabel='Predicted label',
                                     ylabel='True label',
                                     normalize=normalize)

    def get_worst_intent(self, metric: str = 'accuracy', as_graph: bool = False) -> TupleOrAxes:
        """Provides worst intent based on a metric.

        Parameters
        ----------
        metric : str, optional
            Metric to be evaluated against (default is accuracy).
            Can be either of "accuracy", "precision", "recall" or "f1".
        as_graph : bool, optional
            If True, shows the result as a graph, i.e. image (default is false).

        Returns
        -------
        intent : tuple or matplotlib Axes
            Worst intent's name and value.

        Raises
        ------
        KeyError
            If `metric` is any of the expected ones.
        """
        intent, value = self.knowledge_base.get_worst_intent(metric=metric)

        if as_graph:
            text = f'Intent: {intent}\n{metric.capitalize()}: {value:.2f}'
            return plot_text(text=text, title='Worst intent')

        return intent, value

    def get_best_intent(self, metric: str = 'accuracy', as_graph: bool = False) -> TupleOrAxes:
        """Provides best intent based on a metric.

        Parameters
        ----------
        metric : str, optional
            Metric to be evaluated against (default is accuracy).
            Can be either of "accuracy", "precision", "recall" or "f1".
        as_graph : bool, optional
            If True, shows the result as a graph, i.e. image (default is false).

        Returns
        -------
        intent : tuple or matplotlib Axes
            Best intent's name and value.

        Raises
        ------
        KeyError
            If `metric` is any of the expected ones.
        """
        intent, value = self.knowledge_base.get_best_intent(metric=metric)

        if as_graph:
            text = f'Intent: {intent}\n{metric.capitalize()}: {value:.2f}'
            return plot_text(text=text, title='Best intent')

        return intent, value

    def get_classification_report(self, as_dataframe: bool = False) -> DictOrDataframe:
        """Provides classification metrics report.

        Parameters
        ----------
        as_dataframe : bool, optional
            If True, return output as pandas dataframe, otherwise return as dict (default is false).

        Returns
        -------
        classification_report : dict of dict or str | pandas DataFrame.
            Classification metrics report.

        Raises
        ------
        ZeroDivisionError
            If during intent's metrics calculation the denominator evaluates to zero.
        """
        classification_report = self.knowledge_base.get_classification_report()

        if as_dataframe:
            dataframe = pd.DataFrame(data=classification_report).transpose()
            dataframe.loc['accuracy'].iloc[:-1] = 0.

            return dataframe

        return classification_report
