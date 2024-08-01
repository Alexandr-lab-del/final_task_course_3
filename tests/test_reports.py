import pytest
import pandas as pd
from io import StringIO
from src.reports import spending_by_category


@pytest.fixture
def transaction_data():
    csv_data = StringIO("""
Дата операции,Категория,Сумма операции
2022-01-15,Питание,100
2022-02-15,Развлечения,50
2022-03-15,Питание,200
2022-04-15,Питание,150
2022-05-15,Питание,220
    """)
    transactions = pd.read_csv(csv_data, parse_dates=['Дата операции'], dayfirst=True)
    return transactions


@pytest.mark.parametrize(
    "category, test_date, expected_count, expected_data",
    [
        (
                'Питание', '2022-04-15', 3,
                [
                    {'Дата операции': pd.Timestamp('2022-01-15'), 'Категория': 'Питание', 'Сумма операции': 100},
                    {'Дата операции': pd.Timestamp('2022-03-15'), 'Категория': 'Питание', 'Сумма операции': 200},
                    {'Дата операции': pd.Timestamp('2022-04-15'), 'Категория': 'Питание', 'Сумма операции': 150},
                ]
        ),
        (
                'Развлечения', '2022-04-15', 1,
                [
                    {'Дата операции': pd.Timestamp('2022-02-15'), 'Категория': 'Развлечения', 'Сумма операции': 50}
                ]
        ),
        (
                'Питание', '2022-05-15', 3,
                [
                    {'Дата операции': pd.Timestamp('2022-03-15'), 'Категория': 'Питание', 'Сумма операции': 200},
                    {'Дата операции': pd.Timestamp('2022-04-15'), 'Категория': 'Питание', 'Сумма операции': 150},
                    {'Дата операции': pd.Timestamp('2022-05-15'), 'Категория': 'Питание', 'Сумма операции': 220},
                ]
        )
    ]
)
def test_spending_by_category(transaction_data, category, test_date, expected_count, expected_data):
    result = spending_by_category(transaction_data, category, test_date)

    assert len(result) == expected_count, f"Expected {expected_count} rows, but got {len(result)}"

    expected_df = pd.DataFrame(expected_data)

    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected_df)
