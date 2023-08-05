__author__ = 'Milo Utsch'
__version__ = '0.1.0'

import pytest

import pandas as pd

from take_ai_evaluation.logic import validate_ai_base


def test_validation_success():
    mock_df = pd.DataFrame([{'Sentence': 'cadastra ai', 'Intent': 'cadastrar', 'Predicted': 'cadastrar'},
                            {'Sentence': 'compra pra mim', 'Intent': 'compra', 'Predicted': 'cadastrar'},
                            ])
    mock_columns = ['Intent', 'Predicted']

    validate_ai_base(mock_df, mock_columns)
        

def test_validation_missing_col():
    mock_df = pd.DataFrame([{'Sentence': 'cadastra ai', 'entity': 'cadastrar', 'Predicted': 'cadastrar'},
                            {'Sentence': 'compra pra mim', 'entity': 'compra', 'Predicted': 'cadastrar'},
                            ])
    mock_columns = ['Intent', 'Predicted']

    with pytest.raises(KeyError, match=r'.*Dataframe does not contain required column.*'):
        validate_ai_base(mock_df, mock_columns)
        
        
def test_validation_empty_df():
    mock_df = pd.DataFrame()
    
    mock_columns = ['Intent', 'Predicted']

    with pytest.raises(Exception, match=r'.*Dataframe cannot be empty.*'):
        validate_ai_base(mock_df, mock_columns)
