import pandas as pd
from datetime import datetime
from src.utils import load_user_settings, convert_timestamps, load_transactions
from unittest.mock import mock_open, patch
import pytest


@pytest.fixture
def user_settings_data():
    return '{"setting1": "value1"}'


@pytest.fixture
def complex_data():
    return {
        "date": datetime(2023, 1, 1),
        "list": [datetime(2023, 1, 2), datetime(2023, 1, 3)],
        "nested": {
            "date": datetime(2023, 1, 4)
        }
    }


@pytest.fixture
def complex_data_expected():
    return {
        "date": "2023-01-01T00:00:00",
        "list": ["2023-01-02T00:00:00", "2023-01-03T00:00:00"],
        "nested": {
            "date": "2023-01-04T00:00:00"
        }
    }


@pytest.fixture
def transactions_data():
    return {'A': [1, 2], 'B': [3, 4]}


@pytest.mark.parametrize("file_path, expected_result", [
    ('dummy_path', {"setting1": "value1"}),
])
def test_load_user_settings(file_path, expected_result, user_settings_data):
    with patch('builtins.open', mock_open(read_data=user_settings_data)):
        settings = load_user_settings(file_path)
        assert settings == expected_result


@pytest.mark.parametrize("data, expected", [
    ({}, {}),
    ({"date": datetime(2023, 1, 1)}, {"date": "2023-01-01T00:00:00"}),
    pytest.param(None, None, marks=pytest.mark.xfail(reason="None input should fail")),
])
def test_convert_timestamps(data, expected):
    assert convert_timestamps(data) == expected


def test_complex_convert_timestamps(complex_data, complex_data_expected):
    assert convert_timestamps(complex_data) == complex_data_expected


def test_load_transactions(monkeypatch, transactions_data):
    df = pd.DataFrame(transactions_data)

    def mock_read_excel(*args, **kwargs):
        return df

    monkeypatch.setattr(pd, 'read_excel', mock_read_excel)

    result = load_transactions('dummy_path')
    pd.testing.assert_frame_equal(result, df)
