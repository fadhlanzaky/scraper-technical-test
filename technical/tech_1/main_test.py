import main
import pandas as pd
import pytest

def get_params(path:str) -> list:
    df_data_test = pd.read_csv(path)
    return df_data_test.values.tolist()

@pytest.mark.parametrize(
        ('input', 'expected'),
        get_params('data.csv')
)
def test_main(input, expected):
    assert main.initiator_of_discount(input) == expected