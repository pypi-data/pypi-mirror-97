__author__ = 'Milo Utsch'
__version__ = '0.1.0'

import pytest

import pandas as pd

from take_ai_evaluation.persistence import read_dataframe


def test_read_dataframe_from_file():
    pass


def test_read_dataframe_from_powerbi():
    mock_df = pd.DataFrame([{'Sentence': 'cadastra ai', 'Intent': 'cadastrar', 'Predicted': 'cadastrar'},
                            {'Sentence': 'compra pra mim', 'Intent': 'compra', 'Predicted': 'cadastrar'},
                            ])
    
    result = read_dataframe(mock_df)
    
    pd.testing.assert_frame_equal(result, mock_df, check_like=True, check_dtype=False)
