import typing as tp

import pandas as pd

DF = pd.DataFrame


def validate_parameters(params: tp.List, params_names: tp.List[str], target_type: tp.Any) -> None:
    """Validates a list of parameters' types and values.

    Parameters
    ----------
    params
        Parameters to validate.
    params_names: str
        Name of the parameters to be printed in error messages.
    target_type
        Acceptable data types for the parameters.

    Raises
    ------
    TypeError
        If the parameter's type does not match the desired type.
    ValueError
        If the parameter is empty.
    """
    for param, param_name in zip(params, params_names):
        validate_parameter(param=param, param_name=param_name, target_type=target_type)


def validate_parameter(param: tp.Any, param_name: str, target_type: tp.Any) -> None:
    """Validates a parameter's type and value.

    Parameters
    ----------
    param
        Parameter to validate.
    param_name: str
        Name of the parameter to be printed in error messages.
    target_type
        Acceptable data types for the parameter.

    Raises
    ------
    TypeError
        If the parameter's type does not match the desired type.
    ValueError
        If the parameter is empty.
    """
    if not isinstance(param, target_type):
        raise TypeError(f'`{param_name}` must be an instance of {target_type}, not {type(param)}.')

    if not len(param):
        raise ValueError(f'`{param_name}` cannot be empty.')


def validate_dataframe(df: DF, columns: tp.List[str]) -> None:
    """Validates if `df` is not empty and has answer column.

    Parameters
    ----------
    df: pandas.DataFrame
        Dataframe.
    columns: list of str
        Required columns.

    Raises
    ------
    ValueError
        If the `df` is empty.
    AttributeError
        If any of the expected `columns` is not present in `df`.
    """
    if df.empty:
        raise ValueError('Dataframe cannot be empty.')

    for col in columns:
        validate_column(df=df, column=col)


def validate_column(df: DF, column: str) -> None:
    """Validates if `df` has `column`.

    Parameters
    ----------
    df: pandas.DataFrame
        Dataframe.
    column: str
        Target column.

    Raises
    ------
    AttributeError
        If any of the expected columns is not present in `df`.
    """
    if column not in df.columns:
        raise AttributeError(f'Dataframe does not contain required column `{column}`.')
