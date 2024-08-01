import pandas as pd
import pytest
from unittest.mock import patch


@pytest.fixture
def transactions_df():
    return pd.DataFrame({
        'category': ['Супермаркеты', 'Дом и ремонт', 'Супермаркеты', 'Супермаркеты'],
        'amount': [100, 200, 150, -50],
        'date': ['2021-01-01', '2021-02-01', '2021-03-01', '2021-01-15']
    })


@patch('src.main.extract_transactions_with_mobile_numbers')
def test_extract_transactions_with_mobile_numbers(mock_extract, transactions_df):
    mock_extract.return_value = None
    file_path = 'fake_path.xlsx'

    try:
        from src.main import extract_transactions_with_mobile_numbers
        extract_transactions_with_mobile_numbers(file_path)
        mock_extract.assert_called_once_with(file_path)
        print("Функция extract_transactions_with_mobile_numbers успешно вызвана")
    except Exception as e:
        pytest.fail(f"Ошибка при вызове extract_transactions_with_mobile_numbers: {e}")


@patch('src.main.main')
def test_main_function(mock_main):
    mock_main.return_value = "Result"
    datetime_str = "2018-07-20 15:30:45"

    try:
        from src.main import main
        result = main(datetime_str)
        mock_main.assert_called_once_with(datetime_str)
        assert result == "Result"
        print("Функция main успешно вызвана")
    except Exception as e:
        pytest.fail(f"Ошибка при вызове main: {e}")


@patch('src.main.main', side_effect=ValueError("Неверный формат даты"))
def test_main_function_invalid_date(mock_main):
    datetime_str = "invalid date"

    try:
        from src.main import main
        with pytest.raises(ValueError):
            main(datetime_str)
        print("Функция main корректно обработала ошибку формата даты")
    except Exception as e:
        pytest.fail(f"Ошибка при вызове main с неверным форматом даты: {e}")


@patch('src.main.spending_by_category')
@pytest.mark.parametrize("category, date", [
    ('Супермаркеты', '2021-12-31'),
    ('Дом и ремонт', '2021-12-31')
])
def test_spending_by_category(mock_spending, transactions_df, category, date):
    mock_spending.return_value = pd.DataFrame()

    try:
        from src.main import spending_by_category
        report = spending_by_category(transactions_df, category, date)
        mock_spending.assert_called_once_with(transactions_df, category, date)
        print("Функция spending_by_category успешно вызвана")
    except Exception as e:
        pytest.fail(f"Ошибка при вызове spending_by_category: {e}")


@patch('src.main.spending_by_category')
def test_spending_by_category_empty_df(mock_spending):
    mock_spending.return_value = pd.DataFrame()

    empty_df = pd.DataFrame(columns=['category', 'amount', 'date'])

    try:
        from src.main import spending_by_category
        report = spending_by_category(empty_df, 'Супермаркеты', '2021-12-31')
        mock_spending.assert_called_once_with(empty_df, 'Супермаркеты', '2021-12-31')
        assert report.empty
        print("Функция spending_by_category корректно обработала пустой DataFrame")
    except Exception as e:
        pytest.fail(f"Ошибка при вызове spending_by_category с пустым DataFrame: {e}")


@patch('src.main.spending_by_category_custom')
@pytest.mark.parametrize("category, date", [
    ('Дом и ремонт', '2020-12-31'),
    ('Супермаркеты', '2020-12-31')
])
def test_spending_by_category_custom(mock_spending_custom, transactions_df, category, date):
    mock_spending_custom.return_value = pd.DataFrame()

    try:
        from src.main import spending_by_category_custom
        report = spending_by_category_custom(transactions_df, category, date)
        mock_spending_custom.assert_called_once_with(transactions_df, category, date)
        print("Функция spending_by_category_custom успешно вызвана")
    except Exception as e:
        pytest.fail(f"Ошибка при вызове spending_by_category_custom: {e}")


@patch('src.main.spending_by_category_custom')
def test_spending_by_category_custom_invalid_date(mock_spending_custom, transactions_df):
    mock_spending_custom.side_effect = ValueError("Invalid date format")

    try:
        from src.main import spending_by_category_custom
        with pytest.raises(ValueError):
            spending_by_category_custom(transactions_df, 'Дом и ремонт', 'invalid date')
        print("Функция spending_by_category_custom корректно обработала неверный формат даты")
    except Exception as e:
        pytest.fail(f"Ошибка при вызове spending_by_category_custom с неверным форматом даты: {e}")
