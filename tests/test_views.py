import pytest
from unittest.mock import patch, MagicMock
from src.views import fetch_stock_price, get_greeting, get_currency_rates, get_stock_price, analyze_cards
from datetime import datetime
import pandas as pd


@pytest.fixture
def mock_stock_prices():
    return {"AAPL": 150.12}


@pytest.fixture
def mock_api_response():
    return {
        "quotes": {"USDUSD": 1.0, "USDEUR": 0.85},
        "Global Quote": {"05. price": "2725.00"}
    }


@pytest.fixture
def sample_transactions():
    data = {
        'Дата операции': ["01.07.2018 10:00:00", "10.07.2018 10:00:00", "15.07.2018 10:00:00",
                          "20.07.2018 10:00:00"],
        'Сумма операции': [10.0, 20.0, 30.0, 40.0],
        'Категория': ["Food", "Transport", "Food", "Entertainment"],
        'Описание': ["Breakfast", "Bus ticket", "Lunch", "Movie"],
        'Номер карты': ["1234567890123456", "1234567890123456", "6543210987654321", "6543210987654321"]
    }
    df = pd.DataFrame(data)
    df['Дата операции'] = pd.to_datetime(df['Дата операции'], format='%d.%m.%Y %H:%M:%S')
    return df


@pytest.mark.parametrize("stock, expected_price", [
    ("AAPL", 150.12),
    ("MSFT", None)
])
@patch('src.views.default_stock_prices', {"AAPL": 150.12})
def test_fetch_stock_price(stock, expected_price):
    assert fetch_stock_price(stock) == expected_price


@pytest.mark.parametrize("time_str, expected_greeting", [
    ("2023-09-25 09:00:00", "Доброе утро"),
    ("2023-09-25 15:00:00", "Добрый день"),
    ("2023-09-25 20:00:00", "Добрый вечер"),
    ("2023-09-25 02:00:00", "Доброй ночи")
])
def test_get_greeting(time_str, expected_greeting):
    time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    assert get_greeting(time) == expected_greeting


@patch('requests.get')
@patch('src.views.API_KEY', None)
def test_get_currency_rates_no_api_key(mock_get):
    currencies = ["USD", "EUR"]
    rates = get_currency_rates(currencies)
    assert len(rates) == 2
    assert rates[0]["currency"] == "USD"
    assert rates[1]["currency"] == "EUR"


@patch('requests.get')
@patch('src.views.API_KEY', 'test_api_key')
def test_get_currency_rates_with_api_key(mock_get, mock_api_response):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json = MagicMock(return_value=mock_api_response)
    currencies = ["USD", "EUR"]
    rates = get_currency_rates(currencies)
    assert len(rates) == 2
    assert rates[0]["currency"] == "USD"
    assert rates[0]["rate"] == 1.0
    assert rates[1]["currency"] == "EUR"
    assert rates[1]["rate"] == 0.85


@patch('requests.get')
@patch('src.views.API_KEY_STOCK', None)
def test_get_stock_price_no_api_key(mock_get):
    stocks = ["AAPL", "MSFT"]
    prices = get_stock_price(stocks)
    assert len(prices) == 5


@patch('requests.get')
@patch('src.views.API_KEY_STOCK', 'test_api_key')
def test_get_stock_price_with_api_key(mock_get, mock_api_response):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json = MagicMock(return_value=mock_api_response)
    stocks = ["GOOGL"]
    prices = get_stock_price(stocks)
    assert len(prices) == 1
    assert prices[0]["stock"] == "GOOGL"
    assert prices[0]["price"] == 2725.00


@patch('pandas.read_excel')
def test_analyze_cards(mock_read_excel, sample_transactions):
    mock_read_excel.return_value = sample_transactions
    start_date = pd.to_datetime("2018-07-01")
    end_date = pd.to_datetime("2018-07-31")

    card_info, transactions = analyze_cards('/fake/path/operations.xlsx', start_date, end_date)
    assert len(card_info) == 2
    assert len(transactions) == 4
